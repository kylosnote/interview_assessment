import pandas as pd
from difflib import SequenceMatcher

FILE_PATH = r'D:\Users\Rekindle\PycharmProjects\interview_assessment\text-similarity\train.csv'


def main():
    try:
        df = pd.read_csv(FILE_PATH)
        score = []

        # loop through each row to calculate the similarity score
        for index, row in df.iterrows():
            ratio = SequenceMatcher(None,row['description_x'],row['description_y']).ratio()
            score.append(ratio)

        df['score'] = score  # put score into a new column 'score' in dataframe

        df.to_csv('Result.csv', index=False)

    except Exception:
        print("Error")


if __name__ == '__main__':
    main()