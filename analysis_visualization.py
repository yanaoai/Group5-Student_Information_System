import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from database import SessionLocal
from models import Student, Course, Grade, Attendance, WellbeingSurvey
from sqlalchemy import func
from scipy import stats

# Set English font
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False


def get_user_choice():
    """Get user role selection"""
    print(" Student Management System Data Analysis")
    print("=" * 50)
    print("Please select your role:")
    print("1. Health Officer")
    print("2. Course Director")
    print("3. Exit")

    while True:
        choice = input("\nEnter your choice (1/2/3): ").strip()
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("Invalid choice, please try again")


def get_visualization_choice(chart_name):
    """Get choice for generating individual charts"""
    print(f"\nGenerate {chart_name}?")
    print("1. Yes")
    print("2. No")

    while True:
        choice = input("Enter your choice (1/2): ").strip()
        if choice in ['1', '2']:
            return choice
        else:
            print("Invalid choice, please try again")


def get_format_choice():
    """Get output format choice"""
    print("\n Select chart output format:")
    print("1. PNG")
    print("2. PDF")

    while True:
        choice = input("Enter your choice (1/2): ").strip()
        if choice in ['1', '2']:
            return choice
        else:
            print("Invalid choice, please try again")


def shapiro_wilk_normality_test(scores, course_name, alpha=0.05):
    """Perform normality test using Shapiro-Wilk test"""
    try:
        # Perform Shapiro-Wilk normality test
        shapiro_stat, p_value = stats.shapiro(scores)

        # Determine if normally distributed
        is_normal = p_value > alpha
        print(f"    {'Overall grades follow normal distribution' if is_normal else 'Overall grades do not follow normal distribution'}")

        return is_normal, p_value

    except Exception as e:
        print(f"  {course_name} normality test error: {e}")
        return False, 1.0


def generate_health_statistics(session):
    """Generate detailed health data statistical analysis"""
    print("\n" + "=" * 60)
    print(" Health Data Detailed Statistical Analysis")
    print("=" * 60)

    # Get health data
    wellbeing_data = session.query(WellbeingSurvey).all()
    if not wellbeing_data:
        print(" No health survey data available for analysis")
        return None

    # Convert to DataFrame
    health_data = []
    for survey in wellbeing_data:
        health_data.append({
            'week': survey.week_number,
            'stress': survey.stress_level,
            'sleep': survey.hours_slept,
            'student_id': survey.student_id
        })
    df_health = pd.DataFrame(health_data)

    # Basic statistics
    total_records = len(df_health)
    unique_students = df_health['student_id'].nunique()
    unique_weeks = df_health['week'].nunique()

    print(f"\n Data Overview:")
    print(f"  Total records: {total_records}")
    print(f"  Students involved: {unique_students}")
    print(f"  Weeks tracked: {unique_weeks}")

    # Stress level statistics
    print(f"\n Stress Level Analysis (1-5):")
    stress_stats = df_health['stress'].describe()
    stress_percentiles = df_health['stress'].quantile([0.25, 0.5, 0.75])

    print(f"  Mean: {stress_stats['mean']:.2f}")
    print(f"  Median: {stress_stats['50%']:.2f}")
    print(f"  Standard Deviation: {stress_stats['std']:.2f}")
    print(f"  Minimum: {stress_stats['min']:.2f}")
    print(f"  Maximum: {stress_stats['max']:.2f}")
    print(f"  25th Percentile: {stress_percentiles[0.25]:.2f}")
    print(f"  75th Percentile: {stress_percentiles[0.75]:.2f}")

    # Stress level distribution
    stress_distribution = df_health['stress'].value_counts().sort_index()
    print(f"\n  Stress Level Distribution:")
    for level, count in stress_distribution.items():
        percentage = (count / total_records) * 100
        print(f"    Level {level}: {count} times ({percentage:.1f}%)")

    # Sleep time statistics
    print(f"\n Sleep Time Analysis:")
    sleep_stats = df_health['sleep'].describe()
    sleep_percentiles = df_health['sleep'].quantile([0.25, 0.5, 0.75])

    print(f"  Mean: {sleep_stats['mean']:.2f} hours")
    print(f"  Median: {sleep_stats['50%']:.2f} hours")
    print(f"  Standard Deviation: {sleep_stats['std']:.2f} hours")
    print(f"  Minimum: {sleep_stats['min']:.2f} hours")
    print(f"  Maximum: {sleep_stats['max']:.2f} hours")
    print(f"  25th Percentile: {sleep_percentiles[0.25]:.2f} hours")
    print(f"  75th Percentile: {sleep_percentiles[0.75]:.2f} hours")

    # Weekly trend analysis
    print(f"\n Weekly Trend Analysis:")
    weekly_stats = df_health.groupby('week').agg({
        'stress': ['mean', 'std', 'count'],
        'sleep': ['mean', 'std']
    }).round(2)

    for week in sorted(df_health['week'].unique()):
        week_data = df_health[df_health['week'] == week]
        stress_mean = week_data['stress'].mean()
        sleep_mean = week_data['sleep'].mean()
        records = len(week_data)
        print(f"  Week {week}: Stress {stress_mean:.2f}, Sleep {sleep_mean:.2f} hours, Records {records}")

    # Correlation analysis
    correlation = df_health['stress'].corr(df_health['sleep'])
    print(f"\n Stress vs Sleep Correlation Analysis: {correlation:.3f}")
    if correlation < -0.3:
        print(" Stress and sleep show negative correlation")
    elif correlation > 0.3:
        print(" Stress and sleep show positive correlation")
    else:
        print(" Weak correlation between stress and sleep")

    return df_health


def generate_academic_statistics(session):
    """Generate detailed academic data statistical analysis - only course analysis and attendance rates"""
    print("\n" + "=" * 60)
    print(" Academic Data Detailed Statistical Analysis")
    print("=" * 60)

    # Get grade data
    grades = session.query(Grade).all()
    if not grades:
        print(" No grade data available for analysis")
        return None, None, {}

    # Get attendance data
    from models import AttendanceStatus
    attendances = session.query(Attendance).all()

    # Convert to DataFrame
    grade_data = []
    for grade in grades:
        grade_data.append({
            'student_id': grade.student_id,
            'course_id': grade.course_id,
            'score': grade.score,
            'assignment': grade.assignment_title
        })
    df_grades = pd.DataFrame(grade_data)

    attendance_data = []
    for attendance in attendances:
        attendance_data.append({
            'student_id': attendance.student_id,
            'course_id': attendance.course_id,
            'status': attendance.status.value
        })
    df_attendance = pd.DataFrame(attendance_data)

    # Basic statistics
    total_grades = len(df_grades)
    unique_students = df_grades['student_id'].nunique()
    unique_courses = df_grades['course_id'].nunique()

    print(f"\n Data Overview:")
    print(f"  Total grade records: {total_grades}")
    print(f"  Students involved: {unique_students}")
    print(f"  Courses involved: {unique_courses}")

    if not df_attendance.empty:
        total_attendance = len(df_attendance)
        print(f"  Attendance records: {total_attendance}")

    # Course grade statistics
    print(f"\n Course Grade Analysis:")
    course_stats = df_grades.groupby('course_id')['score'].agg([
        'count', 'mean', 'median', 'std', 'min', 'max'
    ]).round(2)

    # Store normality test results for each course
    normality_results = {}

    for course_id, stats in course_stats.iterrows():
        print(f"\n  Course {course_id}:")
        print(f"    Records: {stats['count']}")
        print(f"    Mean: {stats['mean']}")
        print(f"    Median: {stats['median']}")
        print(f"    Standard Deviation: {stats['std']}")
        print(f"    Minimum: {stats['min']}")
        print(f"    Maximum: {stats['max']}")

        # Calculate pass rate (assuming 60 is passing)
        course_scores = df_grades[df_grades['course_id'] == course_id]['score']
        pass_count = len(course_scores[course_scores >= 60])
        pass_rate = (pass_count / stats['count']) * 100
        print(f"    Pass Rate: {pass_rate:.1f}%")

        # Perform Shapiro-Wilk normality test
        if len(course_scores) >= 3:  # Shapiro-Wilk test requires at least 3 data points
            is_normal, p_value = shapiro_wilk_normality_test(course_scores.values, f"Course {course_id}")
            normality_results[course_id] = is_normal
        else:
            print(f"  Course {course_id} insufficient data points for Shapiro-Wilk test")
            normality_results[course_id] = False

    # Course attendance rate statistics
    if not df_attendance.empty:
        print(f"\n Course Attendance Rate Analysis:")

        # Group attendance by course
        course_attendance_stats = df_attendance.groupby('course_id')['status'].agg([
            'count', lambda x: (x == 'present').sum()
        ]).round(2)
        course_attendance_stats.columns = ['total_records', 'present_count']
        course_attendance_stats['attendance_rate'] = (course_attendance_stats['present_count'] /
                                                      course_attendance_stats['total_records']) * 100

        for course_id, stats in course_attendance_stats.iterrows():
            print(f"\n  Course {course_id}:")
            print(f"    Total attendance records: {int(stats['total_records'])}")
            print(f"    Present count: {int(stats['present_count'])}")
            print(f"    Attendance Rate: {stats['attendance_rate']:.1f}%")

            # Count other attendance statuses
            course_attendance = df_attendance[df_attendance['course_id'] == course_id]
            status_counts = course_attendance['status'].value_counts()

            for status, count in status_counts.items():
                if status != 'present':
                    percentage = (count / stats['total_records']) * 100
                    print(f"    {status}: {count} times ({percentage:.1f}%)")

    return df_grades, df_attendance, normality_results


def create_stress_trend_chart(df_health, format_choice):
    """Create stress trend chart"""
    plt.figure(figsize=(12, 8))

    weekly_stress = df_health.groupby('week')['stress'].agg(['mean', 'median', 'std']).reset_index()

    plt.plot(weekly_stress['week'], weekly_stress['mean'], marker='o', linewidth=3,
             label='Average Stress', color='red', markersize=8)
    plt.fill_between(weekly_stress['week'],
                     weekly_stress['mean'] - weekly_stress['std'],
                     weekly_stress['mean'] + weekly_stress['std'],
                     alpha=0.2, color='red', label='Standard Deviation Range')

    plt.title('Weekly Stress Level Trend Analysis', fontsize=16, fontweight='bold')
    plt.xlabel('Week Number', fontsize=12)
    plt.ylabel('Stress Level (1-5)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    plt.ylim(0, 5)
    plt.xticks(weekly_stress['week'])

    filename = 'stress_trend_analysis'
    if format_choice == '1':
        plt.savefig(f'{filename}.png', dpi=300, bbox_inches='tight')
        print(f" Exported: {filename}.png")
    else:
        plt.savefig(f'{filename}.pdf', bbox_inches='tight')
        print(f" Exported: {filename}.pdf")
    plt.close()


def create_sleep_trend_chart(df_health, format_choice):
    """Create sleep trend chart"""
    plt.figure(figsize=(12, 8))

    weekly_sleep = df_health.groupby('week')['sleep'].agg(['mean', 'median', 'std']).reset_index()

    plt.plot(weekly_sleep['week'], weekly_sleep['mean'], marker='s', linewidth=3,
             label='Average Sleep', color='blue', markersize=8)
    plt.fill_between(weekly_sleep['week'],
                     weekly_sleep['mean'] - weekly_sleep['std'],
                     weekly_sleep['mean'] + weekly_sleep['std'],
                     alpha=0.2, color='blue', label='Standard Deviation Range')

    plt.title('Weekly Sleep Time Trend Analysis', fontsize=16, fontweight='bold')
    plt.xlabel('Week Number', fontsize=12)
    plt.ylabel('Sleep Time (hours)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    plt.xticks(weekly_sleep['week'])

    filename = 'sleep_trend_analysis'
    if format_choice == '1':
        plt.savefig(f'{filename}.png', dpi=300, bbox_inches='tight')
        print(f" Exported: {filename}.png")
    else:
        plt.savefig(f'{filename}.pdf', bbox_inches='tight')
        print(f" Exported: {filename}.pdf")
    plt.close()


def create_stress_distribution_chart(df_health, format_choice):
    """Create stress distribution chart"""
    plt.figure(figsize=(10, 6))

    stress_values = df_health['stress'].values
    plt.hist(stress_values, bins=range(1, 7), alpha=0.7, color='lightcoral',
             edgecolor='black', align='left', rwidth=0.8)
    plt.title('Stress Level Distribution', fontsize=16, fontweight='bold')
    plt.xlabel('Stress Level', fontsize=12)
    plt.ylabel('Record Count', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(range(1, 6))

    filename = 'stress_level_distribution'
    if format_choice == '1':
        plt.savefig(f'{filename}.png', dpi=300, bbox_inches='tight')
        print(f" Exported: {filename}.png")
    else:
        plt.savefig(f'{filename}.pdf', bbox_inches='tight')
        print(f" Exported: {filename}.pdf")
    plt.close()


def create_sleep_distribution_chart(df_health, format_choice):
    """Create sleep distribution chart"""
    plt.figure(figsize=(10, 6))

    sleep_values = df_health['sleep'].values
    plt.hist(sleep_values, bins=15, alpha=0.7, color='lightblue',
             edgecolor='black')
    plt.title('Sleep Time Distribution', fontsize=16, fontweight='bold')
    plt.xlabel('Sleep Time (hours)', fontsize=12)
    plt.ylabel('Record Count', fontsize=12)
    plt.grid(True, alpha=0.3)

    filename = 'sleep_time_distribution'
    if format_choice == '1':
        plt.savefig(f'{filename}.png', dpi=300, bbox_inches='tight')
        print(f" Exported: {filename}.png")
    else:
        plt.savefig(f'{filename}.pdf', bbox_inches='tight')
        print(f" Exported: {filename}.pdf")
    plt.close()


def create_course_scores_chart(df_grades, format_choice):
    """Create course scores comparison chart"""
    plt.figure(figsize=(12, 8))

    course_stats = df_grades.groupby('course_id')['score'].agg(['mean', 'median', 'std', 'count']).reset_index()

    x_pos = np.arange(len(course_stats))
    width = 0.35

    # Mean score bar chart
    bars1 = plt.bar(x_pos - width / 2, course_stats['mean'], width, alpha=0.7, color='lightgreen',
                    yerr=course_stats['std'], capsize=5, label='Mean Score')

    # Median score bar chart
    bars2 = plt.bar(x_pos + width / 2, course_stats['median'], width, alpha=0.7, color='lightblue',
                    label='Median Score')

    # Display values on bars
    for i, (mean, median) in enumerate(zip(course_stats['mean'], course_stats['median'])):
        plt.text(i - width / 2, mean + course_stats['std'][i] + 1, f'{mean:.1f}',
                 ha='center', va='bottom', fontsize=10)
        plt.text(i + width / 2, median + 1, f'{median:.1f}',
                 ha='center', va='bottom', fontsize=10)

    plt.title('Course Grade Statistics Comparison', fontsize=16, fontweight='bold')
    plt.xlabel('Course ID', fontsize=12)
    plt.ylabel('Score', fontsize=12)
    plt.xticks(x_pos, [f'Course {cid}' for cid in course_stats['course_id']])
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)

    filename = 'course_scores_comparison'
    if format_choice == '1':
        plt.savefig(f'{filename}.png', dpi=300, bbox_inches='tight')
        print(f" Exported: {filename}.png")
    else:
        plt.savefig(f'{filename}.pdf', bbox_inches='tight')
        print(f" Exported: {filename}.pdf")
    plt.close()


def create_pass_rate_chart(df_grades, format_choice):
    """Create course pass rate chart"""
    plt.figure(figsize=(12, 8))

    course_stats = df_grades.groupby('course_id')['score'].agg(['mean', 'median', 'std', 'count']).reset_index()

    # Calculate pass rates for each course
    pass_rates = []
    course_names = []
    for course_id in course_stats['course_id']:
        course_scores = df_grades[df_grades['course_id'] == course_id]['score']
        pass_count = len(course_scores[course_scores >= 60])
        pass_rate = (pass_count / len(course_scores)) * 100
        pass_rates.append(pass_rate)
        course_names.append(f'Course {course_id}')

    x_pos = np.arange(len(pass_rates))
    bars = plt.bar(x_pos, pass_rates, alpha=0.7, color='orange')

    # Display pass rates on bars
    for i, rate in enumerate(pass_rates):
        plt.text(i, rate + 1, f'{rate:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.title('Course Pass Rate Comparison', fontsize=16, fontweight='bold')
    plt.xlabel('Course ID', fontsize=12)
    plt.ylabel('Pass Rate (%)', fontsize=12)
    plt.xticks(x_pos, course_names)
    plt.ylim(0, 100)
    plt.grid(True, alpha=0.3)

    filename = 'course_pass_rates'
    if format_choice == '1':
        plt.savefig(f'{filename}.png', dpi=300, bbox_inches='tight')
        print(f"  Exported: {filename}.png")
    else:
        plt.savefig(f'{filename}.pdf', bbox_inches='tight')
        print(f"  Exported: {filename}.pdf")
    plt.close()


def create_attendance_rate_chart(df_attendance, format_choice):
    """Create course attendance rate chart"""
    plt.figure(figsize=(12, 8))

    # Group attendance rates by course
    course_attendance_stats = df_attendance.groupby('course_id')['status'].agg([
        'count', lambda x: (x == 'present').sum()
    ]).round(2)
    course_attendance_stats.columns = ['total_records', 'present_count']
    course_attendance_stats['attendance_rate'] = (course_attendance_stats['present_count'] / course_attendance_stats[
        'total_records']) * 100

    attendance_rates = []
    course_names = []
    for course_id in sorted(course_attendance_stats.index):
        rate = course_attendance_stats.loc[course_id, 'attendance_rate']
        attendance_rates.append(rate)
        course_names.append(f'Course {course_id}')

    x_pos = np.arange(len(attendance_rates))
    bars = plt.bar(x_pos, attendance_rates, alpha=0.7, color='lightcoral')

    # Display attendance rates on bars
    for i, rate in enumerate(attendance_rates):
        plt.text(i, rate + 1, f'{rate:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.title('Course Attendance Rate Comparison', fontsize=16, fontweight='bold')
    plt.xlabel('Course ID', fontsize=12)
    plt.ylabel('Attendance Rate (%)', fontsize=12)
    plt.xticks(x_pos, course_names)
    plt.ylim(0, 100)
    plt.grid(True, alpha=0.3)

    filename = 'course_attendance_rates'
    if format_choice == '1':
        plt.savefig(f'{filename}.png', dpi=300, bbox_inches='tight')
        print(f" Exported: {filename}.png")
    else:
        plt.savefig(f'{filename}.pdf', bbox_inches='tight')
        print(f" Exported: {filename}.pdf")
    plt.close()


def create_scores_boxplot(df_grades, format_choice):
    """Create course scores box plot"""
    plt.figure(figsize=(12, 8))

    course_stats = df_grades.groupby('course_id')['score'].agg(['mean', 'median', 'std', 'count']).reset_index()
    course_scores = [df_grades[df_grades['course_id'] == cid]['score'].values
                     for cid in course_stats['course_id']]

    box_plot = plt.boxplot(course_scores, tick_labels=[f'Course {cid}' for cid in course_stats['course_id']],
                           patch_artist=True)

    # Set box plot colors
    for patch in box_plot['boxes']:
        patch.set_facecolor('lightyellow')

    plt.title('Course Grade Distribution Box Plot', fontsize=16, fontweight='bold')
    plt.ylabel('Score', fontsize=12)
    plt.grid(True, alpha=0.3)

    filename = 'course_scores_boxplot'
    if format_choice == '1':
        plt.savefig(f'{filename}.png', dpi=300, bbox_inches='tight')
        print(f" Exported: {filename}.png")
    else:
        plt.savefig(f'{filename}.pdf', bbox_inches='tight')
        print(f" Exported: {filename}.pdf")
    plt.close()


def create_normality_distribution_chart(df_grades, course_id, format_choice):
    """Create normal distribution fit chart for individual course"""
    course_scores = df_grades[df_grades['course_id'] == course_id]['score']

    plt.figure(figsize=(10, 6))

    # Draw histogram
    n, bins, patches = plt.hist(course_scores, bins=20, alpha=0.7, color='skyblue',
                                edgecolor='black', density=True, label='Grade Distribution')

    # Calculate normal distribution parameters
    mu, sigma = np.mean(course_scores), np.std(course_scores)

    # Generate normal distribution curve
    x = np.linspace(min(course_scores), max(course_scores), 100)
    y = stats.norm.pdf(x, mu, sigma)

    # Draw normal distribution curve
    plt.plot(x, y, 'r-', linewidth=2, label=f'Normal Distribution Fit\nμ={mu:.2f}, σ={sigma:.2f}')

    plt.title(f'Course {course_id} Grade Normal Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Score', fontsize=12)
    plt.ylabel('Probability Density', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()

    filename = f'course_{course_id}_normal_distribution'
    if format_choice == '1':
        plt.savefig(f'{filename}.png', dpi=300, bbox_inches='tight')
        print(f" Exported: {filename}.png")
    else:
        plt.savefig(f'{filename}.pdf', bbox_inches='tight')
        print(f" Exported: {filename}.pdf")
    plt.close()

    return f"{filename}.{'png' if format_choice == '1' else 'pdf'}"


def main():
    """Main function"""
    session = SessionLocal()
    try:
        # Select user role
        role_choice = get_user_choice()

        if role_choice == '3':
            return

        # Generate statistical analysis based on role
        if role_choice == '1':  # Health Officer
            df_health = generate_health_statistics(session)
            if df_health is None:
                return

            # Select output format
            format_choice = get_format_choice()

            # Ask for each chart individually
            health_charts = [
                ("Stress Trend Analysis Chart", create_stress_trend_chart),
                ("Sleep Trend Analysis Chart", create_sleep_trend_chart),
                ("Stress Level Distribution Chart", create_stress_distribution_chart),
                ("Sleep Time Distribution Chart", create_sleep_distribution_chart)
            ]

            generated_files = []
            for chart_name, chart_func in health_charts:
                choice = get_visualization_choice(chart_name)
                if choice == '1':
                    chart_func(df_health, format_choice)
                    extension = "png" if format_choice == '1' else "pdf"
                    generated_files.append(f"{chart_name}.{extension}")

            if generated_files:
                print("Exported files:")
                for file in generated_files:
                    print(f"   {file}")
            else:
                print("\n No charts generated")

        else:  # Course Director
            df_grades, df_attendance, normality_results = generate_academic_statistics(session)
            if df_grades is None:
                return

            # Select output format
            format_choice = get_format_choice()

            # Ask for each chart individually
            academic_charts = [
                ("Course Scores Comparison Chart", lambda g, a, f: create_course_scores_chart(g, f)),
                ("Course Pass Rates Chart", lambda g, a, f: create_pass_rate_chart(g, f)),
                ("Course Scores Box Plot", lambda g, a, f: create_scores_boxplot(g, f))
            ]

            # Add attendance rate chart if attendance data exists
            if not df_attendance.empty:
                academic_charts.append(("Course Attendance Rates Chart", lambda g, a, f: create_attendance_rate_chart(a, f)))

            generated_files = []
            for chart_name, chart_func in academic_charts:
                choice = get_visualization_choice(chart_name)
                if choice == '1':
                    chart_func(df_grades, df_attendance, format_choice)
                    extension = "png" if format_choice == '1' else "pdf"
                    generated_files.append(f"{chart_name}.{extension}")

            # Ask to generate normal distribution fit charts for courses that follow normal distribution
            normal_courses = [cid for cid, is_normal in normality_results.items() if is_normal]
            if normal_courses:
                for course_id in normal_courses:
                    chart_name = f"Course {course_id} Normal Distribution Chart"
                    choice = get_visualization_choice(chart_name)
                    if choice == '1':
                        normality_file = create_normality_distribution_chart(df_grades, course_id, format_choice)
                        generated_files.append(normality_file)

            if generated_files:
                print("Exported files:")
                for file in generated_files:
                    print(f"  {file}")
            else:
                print("\n No charts generated")

    except Exception as e:
        print(f" Program execution error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()


if __name__ == "__main__":
    main()