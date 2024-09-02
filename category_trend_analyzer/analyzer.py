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

    def read_trends(self, file_path):
        return pd.read_csv(file_path)

    def trend_count_func(self, trend_counts):
        total_count = trend_counts.sum()
        trend_percentages = (trend_counts / total_count).round(5) * 100
        return {"percentage": trend_percentages}

    def filtered_result(self, country, type, audience, quarter):
        filtered_df = self.df[
            (self.df["Ország"] == country) & 
            (self.df["Típus"] == type) &
            (self.df["Közönség"] == audience) &
            (self.df["Negyedév"] == quarter)
        ]
        trend_counts = filtered_df["Trend"].value_counts().head(10)
        return self.trend_count_func(trend_counts)

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
            print(filtered_result.get("percentage"))

            entry = {
                'Date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Country': country_input,
                'Type': type_input,
                'Audience': audience_input,
                'Quarter': quarter_input
            }
            self.historyCsv(entry)


def main():
    analyzer = TrendsAnalyzer("trends.csv")
    analyzer.analyze()

if __name__ == '__main__':
    main()
