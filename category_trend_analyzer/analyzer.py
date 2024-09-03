import pandas as pd

class TrendsAnalyzer:
    def __init__(self, file_path):
        self.df = self.read_trends(file_path)
        self.countries = self.df["Ország"].unique().tolist()
        self.types = self.df["Típus"].unique().tolist()
        self.df["Year"] = pd.to_datetime(self.df["Dátum"]).dt.year
        self.years = self.df["Year"].unique().tolist()
        self.quarters = [1, 2, 3, 4]
        self.quarters_per_year = [
            (year, quarter) for year in self.years for quarter in self.quarters 
            if (year, quarter) in self.df[['Year', 'Negyedév']].values
        ]
        self.audience = self.df["Közönség"].unique().tolist()

    def historyCsv(self, entry):
        headers = ['Date', 'Country', 'Type', 'Audience', 'Quarter']
        
        df = pd.DataFrame([entry], columns=headers)
        
        df.to_csv("history.csv", index=False, mode='a', header=not pd.io.common.file_exists("history.csv"))
        
    def write_changes_to_csv(self, changes, entry):
        changes_list = []
        for trend, change in changes.items():
            changes_list.append({
                'Date': entry['Date'],
                'Country': entry['Country'],
                'Type': entry['Type'],
                'Audience': entry['Audience'],
                'Quarter': entry['Quarter'],
                'Year': entry['Year'],
                'Trend': trend,
                'Change': change
            })

        changes_df = pd.DataFrame(changes_list)
        changes_file = "trend_changes.csv"

        changes_df.to_csv(changes_file, index=False, mode='a', header=not pd.io.common.file_exists(changes_file), encoding='utf-8-sig')

    def read_trends(self, file_path) -> pd.DataFrame:
        return pd.read_csv(file_path)

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
                changes[trend] = f"{change_value:+d}"
            else:
                changes[trend] = "new entry"

        for trend in previous_ranking:
            if trend not in current_trends:
                changes[trend] = f"left top 10 (was {previous_ranking[trend]})"

        return changes

    def get_rankings(self, df, quarter):
        filtered_df = df[(df["Negyedév"] == quarter)]
        return filtered_df["Trend"].value_counts().index.tolist()

    def get_previous_quarter(self, year, quarter):
        if quarter == 1:
            previous_quarter = 4
            previous_year = year - 1
        else:
            previous_quarter = quarter - 1
            previous_year = year
        # Check if the (previous_year, previous_quarter) exists in the data
        if (previous_year, previous_quarter) in self.quarters_per_year:
            return previous_year, previous_quarter
        else:
            return None, None

    def filtered_result(self, country, type, audience, quarter, year):
        # Filter the DataFrame based on the given filters
        current_df = self.df[
            (self.df["Ország"] == country) & 
            (self.df["Típus"] == type) &
            (self.df["Közönség"] == audience) &
            (self.df["Negyedév"] == quarter) &
            (self.df["Year"] == year)
        ]
        
        print("Current df:", current_df, "\n")
        
        # Count the occurrences of each trend in the current DataFrame and sort to get the top 10 trends
        trend_counts = current_df["Trend"].value_counts().head(10)
        current_trends = trend_counts.index.tolist()
        print("Current trends:", current_trends, "\n")

        # Determine the previous year and quarter to compare with
        prev_year, prev_quarter = self.get_previous_quarter(year, quarter)

        if prev_year is None or prev_quarter is None:
            trend_changes = {}
        else:
            # Filter the DataFrame for the previous quarter and year
            previous_df = self.df[
                (self.df["Ország"] == country) & 
                (self.df["Típus"] == type) &
                (self.df["Közönség"] == audience) &
                (self.df["Negyedév"] == prev_quarter) &
                (self.df["Year"] == prev_year)
            ]
            # Get the top 10 trends from the previous quarter
            previous_trend_counts = previous_df["Trend"].value_counts().head(10)
            previous_trends = previous_trend_counts.index.tolist()
            print("Previous trends:", previous_trends, "\n")
            
            # Compare only the top 10 trends of the current and previous quarters
            trend_changes = self.compare_trends(current_trends, previous_trends)
            print("Trend changes:", trend_changes, "\n")

        # Create a DataFrame for the top 10 trends with their changes
        top10_df = pd.DataFrame({
            'Trend': current_trends
        })

        # Map the changes and percentages to the top 10 trends DataFrame
        top10_df['Change'] = top10_df['Trend'].map(trend_changes).fillna("no change")
        trend_percentages = self.trend_count_func(trend_counts)
        print("Trend percentages:", trend_percentages, "\n")
        top10_df['Percentage'] = top10_df['Trend'].map(trend_percentages).fillna(0)

        return top10_df

    def analyze(self):
        while True:
            print("----------------------")
            print("----TREND ANALYZER----")
            print("----------------------")
            print("Top 10 trend analysis")
            print("Countries to choose from: ", [(index + 1, country) for index, country in enumerate(self.countries)], "\n")
            print("Types to choose from: ", [(index + 1, dfType) for index, dfType in enumerate(self.types)], "\n")
            print("Audience to choose from: ", [(index + 1, audience) for index, audience in enumerate(self.audience)], "\n")
            print("Please enter the filters in the order of (int) -> [country, type, audience, quarter, year]:")
            choice_input = input("Enter your choice: ")

            choice_input = list(map(int, choice_input.split()))
            country_input = self.countries[choice_input[0] - 1]
            type_input = self.types[choice_input[1] - 1]
            audience_input = self.audience[choice_input[2] - 1]
            quarter_input = choice_input[3]
            year_input = choice_input[4]

            print("Selected:", country_input, type_input, audience_input, quarter_input, year_input)

            filtered_result = self.filtered_result(country_input, type_input, audience_input, quarter_input, year_input)
            print(filtered_result)

            entry = {
                'Date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Country': country_input,
                'Type': type_input,
                'Audience': audience_input,
                'Year': year_input,
                'Quarter': quarter_input
            }
            self.historyCsv(entry)
            self.write_changes_to_csv(filtered_result.set_index('Trend')['Change'].to_dict(), entry)

def main():
    analyzer = TrendsAnalyzer("trends.csv")
    analyzer.analyze()

if __name__ == '__main__':
    main()
