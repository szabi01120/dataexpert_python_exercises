import pandas as pd


class TrendDataHandler:    
    def __init__(self, file_path):
        self.df = self.read_trends(file_path)
        self.df["Year"] = pd.to_datetime(self.df["Dátum"]).dt.year

    def read_trends(self, file_path) -> pd.DataFrame:
        return pd.read_csv(file_path)

    def save_to_csv(self, data, file_name, mode='a', header=False):
        data.to_csv(file_name, index=False, mode=mode, header=header, encoding='utf-8-sig')

class TrendAnalyzer:    
    def __init__(self, data_handler: TrendDataHandler):
        self.df = data_handler.df
        self.countries = self.df["Ország"].unique().tolist()
        self.types = self.df["Típus"].unique().tolist()
        self.years = self.df["Year"].unique().tolist()
        self.quarters = [1, 2, 3, 4]
        self.quarters_per_year = [
            (year, quarter) for year in self.years for quarter in self.quarters
            if (year, quarter) in self.df[['Year', 'Negyedév']].values
        ]
        self.audience = self.df["Közönség"].unique().tolist()
        self.data_handler = data_handler

    def filter_data(self, country, type_input, audience, quarter, year):
        return self.df[
            (self.df["Ország"] == country) &
            (self.df["Típus"] == type_input) &
            (self.df["Közönség"] == audience) &
            (self.df["Negyedév"] == quarter) &
            (self.df["Year"] == year)
        ]

    def trend_count_func(self, trend_counts):
        total_count = trend_counts.sum()
        trend_percentages = (trend_counts / total_count) * 100
        return trend_percentages

    def compare_trends(self, current_trends, previous_trends):
        changes = {}
        previous_ranking = {trend: rank + 1 for rank, trend in enumerate(previous_trends)}

        for rank, trend in enumerate(current_trends):
            current_rank = rank + 1
            if trend in previous_ranking:
                prev_rank = previous_ranking[trend]
                change_value = prev_rank - current_rank
                changes[trend] = f"{change_value:+d}" if change_value != 0 else "no change"
            else:
                changes[trend] = "new entry"

        for trend in previous_ranking:
            if trend not in current_trends:
                changes[trend] = f"left top 10 (was {previous_ranking[trend]})"

        return changes

    def get_previous_quarter(self, year, quarter):
        if quarter == 1:
            return year - 1, 4
        return year, quarter - 1

    def filtered_result(self, country, type_input, audience, quarter, year):
        current_df = self.filter_data(country, type_input, audience, quarter, year)
        trend_counts = current_df["Trend"].value_counts().head(10)  # Get top 10 trends
        current_trends = trend_counts.index.tolist()  # List of current top 10 trends

        prev_year, prev_quarter = self.get_previous_quarter(year, quarter)
        
        if (prev_year, prev_quarter) not in self.quarters_per_year:
            trend_changes = {}  # No previous data available
        else:
            previous_df = self.filter_data(country, type_input, audience, prev_quarter, prev_year)
            previous_trends = previous_df["Trend"].value_counts().head(10).index.tolist()  # Previous top 10 trends
            trend_changes = self.compare_trends(current_trends, previous_trends)

        top10_df = pd.DataFrame({
            'Trend': current_trends
        })

        top10_df['Change'] = top10_df['Trend'].map(trend_changes).fillna("no change")
        trend_percentages = self.trend_count_func(trend_counts)
        top10_df['Percentage'] = top10_df['Trend'].map(trend_percentages).fillna(0) # Fill NaN values with 0

        return top10_df

    def result_summary(self, country_input, type_input, audience_input, quarter_input, year_input):
        filtered_result = self.filtered_result(country_input, type_input, audience_input, quarter_input, year_input)

        entry = {
            'Date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Country': country_input,
            'Type': type_input,
            'Audience': audience_input,
            'Year': year_input,
            'Quarter': quarter_input
        }
        
        self.data_handler.save_to_csv(pd.DataFrame([entry]), "history.csv", header=not pd.io.common.file_exists("history.csv"))
        changes_dict = filtered_result.set_index('Trend')['Change'].to_dict()
        changes_list = [{'Trend': trend, 'Change': change, **entry} for trend, change in changes_dict.items()]
        self.data_handler.save_to_csv(pd.DataFrame(changes_list), "trend_changes.csv", header=not pd.io.common.file_exists("trend_changes.csv"))

    def apply_filters_across_countries(self, trend, type_input, audience_input, quarter_input, year_input):
        total_count = 0
        country_counts = {}

        for country in self.countries:
            filtered_df = self.filter_data(country, type_input, audience_input, quarter_input, year_input)
            trend_count = filtered_df["Trend"].value_counts().get(trend, 0)
            total_count += trend_count
            country_counts[country] = trend_count

        country_percentages = {country: (count / total_count) * 100 if total_count > 0 else 0
                               for country, count in country_counts.items()}

        result_df = pd.DataFrame.from_dict(country_percentages, orient='index', columns=['Percentage']).reset_index().round(3)
        result_df = result_df.rename(columns={'index': 'Country'})
        result_df = result_df.sort_values(by='Percentage', ascending=False)
        result_df = result_df[result_df['Percentage'] != 0]
        
        print(f"\nSummary of the trend '{trend}' across all countries:\n")
        print(result_df)

        self.data_handler.save_to_csv(result_df, "trend_summary_across_countries.csv")

class UserInterface:    
    def __init__(self, trend_analyzer: TrendAnalyzer):
        self.analyzer = trend_analyzer

    def render_start(self):
        print("----------------------")
        print("----TREND ANALYZER----")
        print("----------------------")
        print("Top 10 trend analysis")

    def display_options(self):
        # options for filtering
        countries = [(index + 1, country) for index, country in enumerate(self.analyzer.countries)]
        types = [(index + 1, df_type) for index, df_type in enumerate(self.analyzer.types)]
        audience = [(index + 1, aud) for index, aud in enumerate(self.analyzer.audience)]

        print("Countries to choose from:", countries, "\n")
        print("Types to choose from:", types, "\n")
        print("Audience to choose from:", audience, "\n")

    def split_input(self, input_list):
        filters_input = list(map(int, input_list.split()))

        country_input = self.analyzer.countries[filters_input[0] - 1]
        type_input = self.analyzer.types[filters_input[1] - 1]
        audience_input = self.analyzer.audience[filters_input[2] - 1]
        quarter_input = filters_input[3]
        year_input = filters_input[4]

        return country_input, type_input, audience_input, quarter_input, year_input

    def analyze(self):
        self.render_start()
        self.display_options()
        chosen_options_list = input("Enter the filters in the order of (int) -> [country, type, audience, quarter, year]: ")
        country_input, type_input, audience_input, quarter_input, year_input = self.split_input(chosen_options_list)
        filtered_result = self.analyzer.filtered_result(country_input, type_input, audience_input, quarter_input, year_input)
                
        print(filtered_result)

        while True:
            self.render_start()
            print("Choose from the following options:")
            print("1.) Filter summary data")
            print("2.) Filter a specific trend")
            choice_input = input("Enter your choice: ")
            print()

            if choice_input == "1":
                self.display_options()
                filters_input = input("Enter your choice (int) -> [country, type, audience, quarter, year]: ")
                country_input, type_input, audience_input, quarter_input, year_input = self.split_input(filters_input)

                filtered_result = self.analyzer.filtered_result(country_input, type_input, audience_input, quarter_input, year_input)
                
                print(filtered_result)
                
                self.analyzer.result_summary(country_input, type_input, audience_input, quarter_input, year_input)

            elif choice_input == "2":
                filtered_result = self.analyzer.filtered_result(country_input, type_input, audience_input, quarter_input, year_input)

                trends = filtered_result['Trend'].tolist()
                trend_options = [(index + 1, trend) for index, trend in enumerate(trends)]
                print("Trends to choose from:", trend_options)

                trend_choice = int(input("Choose a trend by number: "))
                selected_trend = trends[trend_choice - 1]

                self.analyzer.apply_filters_across_countries(selected_trend, type_input, audience_input, quarter_input, year_input)

def main():
    data_handler = TrendDataHandler("trends.csv")
    analyzer = TrendAnalyzer(data_handler)
    ui = UserInterface(analyzer)
    ui.analyze()

if __name__ == '__main__':
    main()
