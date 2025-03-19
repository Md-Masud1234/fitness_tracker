import json
import os
import datetime
import matplotlib.pyplot as plt

DATA_FILE = "fitness_data.json"

class Workout:
    def __init__(self, workout_type, duration, calories, date=None):
        self.workout_type = workout_type
        self.duration = duration
        self.calories = calories
        self.date = date or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "workout_type": self.workout_type,
            "duration": self.duration,
            "calories": self.calories,
            "date": self.date
        }

    def __str__(self):
        return f"[{self.date}] {self.workout_type} - {self.duration} min - {self.calories} cal"

class FitnessTracker:
    def __init__(self):
        self.workout_history = []
        self.daily_goal = 500  # Default daily calorie burn goal
        self.load_data()

    def add_workout(self, workout_type, duration, calories):
        workout = Workout(workout_type, duration, calories)
        self.workout_history.append(workout)
        self.save_data()
        print("\n✅ Workout added successfully!\n")

    def view_history(self):
        if not self.workout_history:
            print("\nNo workouts logged yet.\n")
            return
        print("\n📜 Workout History:")
        for workout in self.workout_history:
            print(workout)
        print()

    def total_calories_burned(self):
        total = sum(workout.calories for workout in self.workout_history)
        print(f"\n🔥 Total Calories Burned: {total} cal\n")

    def save_data(self):
        data = [workout.to_dict() for workout in self.workout_history]
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                for item in data:
                    workout = Workout(**item)
                    self.workout_history.append(workout)

    def plot_progress(self):
        if not self.workout_history:
            print("\nNo data to plot.\n")
            return

        dates = [workout.date.split(' ')[0] for workout in self.workout_history]
        calories = [workout.calories for workout in self.workout_history]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, calories, marker='o', linestyle='-', color='b')
        plt.xticks(rotation=45)
        plt.title("Calories Burned Over Time")
        plt.xlabel("Date")
        plt.ylabel("Calories Burned")
        plt.tight_layout()
        plt.grid(True)
        plt.show()

    def bmi_calculator(self, weight, height_cm):
        height_m = height_cm / 100
        bmi = weight / (height_m ** 2)
        print(f"\n🧮 Your BMI is: {bmi:.2f}")
        if bmi < 18.5:
            print("Status: Underweight")
        elif 18.5 <= bmi < 24.9:
            print("Status: Normal weight")
        elif 25 <= bmi < 29.9:
            print("Status: Overweight")
        else:
            print("Status: Obese")
        print()

    def check_daily_goal(self):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        calories_today = sum(w.calories for w in self.workout_history if w.date.startswith(today))
        print(f"\n🎯 Today's Calories Burned: {calories_today} cal")
        if calories_today >= self.daily_goal:
            print("✅ Congrats! You achieved your daily goal!\n")
        else:
            print(f"❌ You are {self.daily_goal - calories_today} cal away from your goal.\n")

    def set_daily_goal(self, new_goal):
        self.daily_goal = new_goal
        print(f"\n✅ Daily calorie goal set to {new_goal} cal.\n")

def main():
    tracker = FitnessTracker()
    while True:
        print("\n===== Personal Fitness Tracker =====")
        print("1. Add Workout")
        print("2. View Workout History")
        print("3. Total Calories Burned")
        print("4. Plot Progress")
        print("5. BMI Calculator")
        print("6. Check Daily Calorie Goal")
        print("7. Set Daily Calorie Goal")
        print("8. Exit")
        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            workout_type = input("Enter workout type (e.g., Running, Cycling, Yoga): ")
            duration = int(input("Enter duration (in minutes): "))
            calories = int(input("Enter calories burned: "))
            tracker.add_workout(workout_type, duration, calories)

        elif choice == '2':
            tracker.view_history()

        elif choice == '3':
            tracker.total_calories_burned()

        elif choice == '4':
            tracker.plot_progress()

        elif choice == '5':
            weight = float(input("Enter your weight (in kg): "))
            height = float(input("Enter your height (in cm): "))
            tracker.bmi_calculator(weight, height)

        elif choice == '6':
            tracker.check_daily_goal()

        elif choice == '7':
            new_goal = int(input("Set your new daily calorie goal: "))
            tracker.set_daily_goal(new_goal)

        elif choice == '8':
            print("\nThank you for using the Fitness Tracker. Stay healthy! 💪")
            break

        else:
            print("\nInvalid choice. Please try again.\n")

if __name__ == "__main__":
    main()
