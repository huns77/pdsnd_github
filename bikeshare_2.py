
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    
    
    print('안녕하세요! 미국의 자전거 공유 데이터를 살펴봅시다!')
    
    # 사용자로부터 도시 입력 받기 (chicago, new york city, washington). 힌트: 잘못된 입력 처리를 위해 while 루프 사용
    while True:
        city = input('도시를 선택하세요 (chicago, new york city, washington): ')
        if city.lower() in CITY_DATA:
            break
        else:
            print('잘못된 입력입니다. 다시 입력하세요.')

    # 사용자로부터 월 입력 받기 (all, january, february, ... , june)
    # 1월, 2월, 3월, 4월, 5월, 6월 등 모든 월을 리스트항목으로 가지는 month
    while True:
        month = input('월을 선택하세요 (all, january, february, ... ): ')
        if month.lower() in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('잘못된 입력입니다. 다시 입력하세요.')

    # 사용자로부터 요일 입력 받기 (all, monday, tuesday, ... sunday)
    # 월요일, 화요일, 수요일, 목요일, 금요일, 토요일, 일요일 모든요일을 항목으로 가지는 DAYS
    while True:
        day = input('요일을 선택하세요 (all, monday, tuesday, ... sunday): ')
        if day.lower() in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print('잘못된 입력입니다. 다시 입력하세요.')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    지정된 도시에 대한 데이터를 로드하고 적용 가능한 경우 월 및 요일로 필터링합니다.

    인수:
        (str) city - 분석할 도시의 이름
        (str) month - 필터링할 월의 이름 또는 "all" (월에 대한 필터 없음)
        (str) day - 필터링할 요일의 이름 또는 "all" (요일에 대한 필터 없음)
    반환:
        df - 월 및 요일로 필터링된 도시 데이터를 포함하는 Pandas DataFrame
    """
    # 데이터 파일을 데이터프레임으로 로드
    df = pd.read_csv(CITY_DATA[city])

    # 'Start Time' 열을 datetime 형식으로 변환
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # '월' 및 '요일' 열 추가
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # 월에 따라 필터링
    if month.lower() != 'all':
        month_num = ['january', 'february', 'march', 'april', 'may', 'june'].index(month.lower()) + 1
        df = df[df['Month'] == month_num]

    # 요일에 따라 필터링
    if day.lower() != 'all':
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """가장 빈번한 시간에 대한 통계를 표시합니다."""

    print('\n가장 빈번한 시간 계산 중...\n')
    start_time = time.time()

    # 가장 일반적인 월 표시
    common_month = df['Month'].mode()[0]
    print(f'가장 일반적인 월: {common_month}월')

    # 가장 일반적인 요일 표시
    common_day = df['Day of Week'].mode()[0]
    print(f'가장 일반적인 요일: {common_day}')

    # 가장 일반적인 시작 시간 표시
    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].mode()[0]
    print(f'가장 일반적인 시작 시간: {common_hour}시')

    print("\n소요 시간: %s 초." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """가장 인기 있는 역 및 여행에 대한 통계를 표시합니다."""

    print('\n가장 인기 있는 역 및 여행 계산 중...\n')
    start_time = time.time()

    # 가장 일반적으로 사용되는 시작 역 표시
    common_start_station = df['Start Station'].mode()[0]
    print(f'가장 일반적으로 사용되는 시작 역: {common_start_station}')

    # 가장 일반적으로 사용되는 종료 역 표시
    common_end_station = df['End Station'].mode()[0]
    print(f'가장 일반적으로 사용되는 종료 역: {common_end_station}')

    # 시작 역과 종료 역 여행의 가장 빈도 높은 조합 표시
    common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f'가장 빈도 높은 시작 및 종료 역 조합: {common_trip}')

    print("\n소요 시간: %s 초." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """총 여행 시간 및 평균 여행 시간에 대한 통계를 표시합니다."""

    print('\n여행 시간 계산 중...\n')
    start_time = time.time()

    # 총 여행 시간 표시
    total_travel_time = df['Trip Duration'].sum()
    print(f'총 여행 시간: {total_travel_time} 초')

    # 평균 여행 시간 표시
    mean_travel_time = df['Trip Duration'].mean()
    print(f'평균 여행 시간: {mean_travel_time} 초')

    print("\n소요 시간: %s 초." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """자전거 공유 사용자에 대한 통계를 표시합니다."""

    print('\n사용자 통계 계산 중...\n')
    start_time = time.time()

    # 사용자 유형 수 표시
    user_type_counts = df['User Type'].value_counts()
    print(f'사용자 유형 수:\n{user_type_counts}\n')

    # 성별 수 표시 (이용 가능한 경우)
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print(f'성별 수:\n{gender_counts}\n')
    else:
        print('이 도시에는 성별 정보가 없습니다.')

    # 가장 일찍, 가장 최근 및 가장 일반적인 출생 연도 표시 (이용 가능한 경우)
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        print(f'가장 일찍 태어난 연도: {earliest_birth_year}\n가장 최근에 태어난 연도: {most_recent_birth_year}\n가장 일반적인 출생 연도: {common_birth_year}')
    else:
        print('이 도시에는 출생 연도 정보가 없습니다.')

    print("\n소요 시간: %s 초." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\n다시 시작하시겠습니까? yes 또는 no를 입력하세요.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
