import pandas as pd

class TrendsAnalyzer:
    def __init__(self, file_path):
        self.df = self.read_trends(file_path)
        self.countries = self.df["Ország"].unique().tolist()
        self.types = self.df["Típus"].unique().tolist()
        self.audience = self.df["Közönség"].unique().tolist()
        self.quarters = [1, 2, 3, 4]

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
                'Trend': trend,
                'Change': change
            })

        changes_df = pd.DataFrame(changes_list)
        changes_file = "trend_changes.csv"

        changes_df.to_csv(changes_file, index=False, mode='a', header=not pd.io.common.file_exists(changes_file))

    def read_trends(self, file_path):
        return pd.read_csv(file_path)

    def trend_count_func(self, trend_counts):
        total_count = trend_counts.sum()
        trend_percentages = (trend_counts / total_count).round(5) * 100
        return trend_percentages.to_dict()

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
        filtered_df = df[
            (df["Negyedév"] == quarter)
        ]
        return filtered_df["Trend"].value_counts().head(10).index.tolist()

    def filtered_result(self, country, type, audience, quarter):
        current_df = self.df[
            (self.df["Ország"] == country) & 
            (self.df["Típus"] == type) &
            (self.df["Közönség"] == audience) &
            (self.df["Negyedév"] == quarter)
        ]
        current_trends = self.get_rankings(current_df, quarter)
        print("Current trends:", current_trends, "\n")

        if quarter == 1:
            trend_changes = {}
        else:
            previous_quarter = quarter - 1
            previous_df = self.df[
                (self.df["Ország"] == country) & 
                (self.df["Típus"] == type) &
                (self.df["Közönség"] == audience) &
                (self.df["Negyedév"] == previous_quarter)
            ]
            previous_trends = self.get_rankings(previous_df, previous_quarter)
            print("Previous trends:", previous_trends, "\n")
            trend_changes = self.compare_trends(current_trends, previous_trends)
            print("Trend changes:", trend_changes, "\n")

        top10_df = pd.DataFrame({
            'Trend': current_trends
        })

        top10_df['Change'] = top10_df['Trend'].map(trend_changes).fillna("no change")

        trend_counts = pd.Series(current_trends).value_counts()
        trend_percentages = self.trend_count_func(trend_counts)
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
            print("Please enter the filters in the order of (int) -> [country, type, audience, quarter]:")
            choice_input = input("Enter your choice: ")

            choice_input = list(map(int, choice_input.split()))
            country_input = self.countries[choice_input[0] - 1]
            type_input = self.types[choice_input[1] - 1]
            audience_input = self.audience[choice_input[2] - 1]
            quarter_input = choice_input[3]

            print("Selected:", country_input, type_input, audience_input, quarter_input)

            filtered_result = self.filtered_result(country_input, type_input, audience_input, quarter_input)
            print(filtered_result)

            entry = {
                'Date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Country': country_input,
                'Type': type_input,
                'Audience': audience_input,
                'Quarter': quarter_input
            }
            self.historyCsv(entry)
            self.write_changes_to_csv(filtered_result.set_index('Trend')['Change'].to_dict(), entry)

def main():
    analyzer = TrendsAnalyzer("trends.csv")
    analyzer.analyze()

if __name__ == '__main__':
    main()
