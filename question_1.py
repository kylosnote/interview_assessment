import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

FILE_PATH = r"D:\Users\Rekindle\PycharmProjects\interview_assessment\online-job-postings\data job posts.csv"
STOP_WORDS = set(stopwords.words('english'))


def sanitize_word(words):
    clean_word = [w for w in words.lower().split() if w not in STOP_WORDS] # list comprehension remove stopwords
    wnl = WordNetLemmatizer()
    singularized = [wnl.lemmatize(w) for w in clean_word]
    return " ".join(singularized)


def find_max_ads_company_per_year(df):
    year_range = df['Year'].unique().tolist()
    company_list = []
    score_list = []

    company_counts = df.groupby(['Year', 'Company']).size()
    company_most = company_counts.max(level=['Year', 'Company'])

    for year in year_range:
        company_list.append(company_most[year].idxmax(axis=0))
        score_list.append(company_most[year, company_most[year].idxmax(axis=0)])

    most_ads_company_dataset = list(zip(year_range,company_list,score_list))
    most_ads_company_df = pd.DataFrame(data=most_ads_company_dataset,columns=['Year','Company','Total'])
    print(most_ads_company_df[-2:])
    most_ads_company_df[-2:].to_csv('MostAdsCompanyPerYear.csv', index=False)


def find_max_ads_month_per_year(df):
    month_counts = df.groupby(['Year','Month']).size()
    year_most = month_counts.max(level=['Year'])

    year_list = []
    month_list = []
    score_list = []

    for year,score in year_most.iteritems():
        year_list.append(year)
        score_list.append(score)

    for year in year_list:
        month_list.append(month_counts[year].idxmax(axis=0))

    most_job_month_dataset = list(zip(year_list, month_list, score_list))
    most_job_month_df = pd.DataFrame(data=most_job_month_dataset, columns=['Year','Month','Total'])
    print(most_job_month_df)
    most_job_month_df.to_csv('MostAdsMonthPerYear.csv', index=True)


def main():
    try:
        print("Start")
        df = pd.read_csv(FILE_PATH)

        job_index = df.shape[0]
        job_title = df['Title'].tolist()
        position_duration = df['Duration'].tolist()
        position_location = df['Location'].tolist()
        job_description = df['JobDescription'].tolist()
        job_responsibilities = df['JobRequirment'].tolist()
        required_qualifications = df['RequiredQual'].tolist()
        remuneration = df['Salary'].tolist()
        application_deadline = df['Deadline'].tolist()
        about_company = df['AboutC'].tolist()
        company = df['Company'].tolist()
        month = df['Month'].tolist()

        # find company with most ads every year
        find_max_ads_company_per_year(df=df)

        # find month with most ads every year
        find_max_ads_month_per_year(df=df)

        sanitized_required_qualifications = []
        for sentence in required_qualifications:
            sanitized_required_qualifications.append(sanitize_word(str(sentence)))

        job_post_dataset = list(zip(job_title, position_duration, position_location,
                                    job_description, job_responsibilities, sanitized_required_qualifications,
                                    remuneration, application_deadline, about_company,
                                    ))

        job_post_df = pd.DataFrame(data=job_post_dataset,
                                   columns=["Job Title", "Position Duration", "Position Location", "Job Description",
                                            "Job Responsibilities", "Required Qualifications", "Remuneration",
                                            "Application Deadline", "About Company"])

        job_post_df.to_csv('FinalJobPost.csv', index=True)

        print("End")
    except Exception as ex:
        print(str(ex))


if __name__ == '__main__':
    main()