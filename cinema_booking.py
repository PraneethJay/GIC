class CinemaBookingSystem:
    def __init__(self):
        self.movie_title = ""
        self.seating_map = []
        self.bookings = {}
        self.seating_capacity = 0
        self.booking_id_counter = 1

    def start(self):
        print("Please define movie title and seating map in [Title] [Row] [SeatsPerRow] format:")
        while True:
            user_input = input("> ").split()

            if len(user_input) != 3:
                print("Invalid input. Please enter in the format: [Title] [Row] [SeatsPerRow]")
                continue

            self.movie_title = user_input[0]

            try:
                rows = int(user_input[1])
                seats_per_row = int(user_input[2])

                if rows > 26 or rows < 1:
                    print("The number of rows must be between 1 and 26.")
                    continue
                if seats_per_row > 50 or seats_per_row < 1:
                    print("The number of seats per row must be between 1 and 50.")
                    continue

                self.seating_capacity = rows * seats_per_row
                self.seating_map = [['.' for _ in range(seats_per_row)] for _ in range(rows)]
                break
            except ValueError:
                print("Invalid input. Please enter a valid format: [Title] [Row] [SeatsPerRow]")

        self.main_menu()

    def main_menu(self):
        while True:
            print(f"\nWelcome to GIC Cinemas\n[1] Book tickets for {self.movie_title} ({self.seating_capacity} seats available)\n[2] Check bookings\n[3] Exit\nPlease enter your selection:")
            choice = input("> ")

            if choice == "1":
                self.book_ticket()
            elif choice == "2":
                self.check_bookings()
            elif choice == "3":
                print("Thank you for using GIC Cinemas system. Bye!")
                break

    def book_ticket(self):
        while True:
            print(f"\nEnter number of tickets to book, or enter blank to go back to main menu:")
            try:
                num_tickets = input("> ").strip()
                if not num_tickets:
                    break

                num_tickets = int(num_tickets)

                if num_tickets > self.seating_capacity:
                    print(f"Sorry, there are only {self.seating_capacity} seats available.")
                    continue

                booking_id = f"GIC{self.booking_id_counter:04d}"
                self.booking_id_counter += 1

                print(f"\nSuccessfully reserved {num_tickets} {self.movie_title} tickets.")
                print(f"Booking id: {booking_id}")
                selected_seats = self.allocate_seats(num_tickets)
                self.bookings[booking_id] = selected_seats

                self.display_seats(selected_seats)

                print("\nEnter blank to accept seat selection, or enter new seating position:")
                new_position = input("> ").strip()

                if new_position:
                    selected_seats = self.relocate_seats(new_position, num_tickets)
                    self.bookings[booking_id] = selected_seats

                    self.display_seats(selected_seats)

                print(f"\nBooking id: {booking_id} confirmed.")

                # Mark selected seats with '#' to indicate they're booked
                for r, c in selected_seats:
                    self.seating_map[r][c] = '#'

                self.seating_capacity -= num_tickets
                self.display_seats()
                break

            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def check_bookings(self):
        while True:
            print(f"\nEnter booking id, or enter blank to go back to main menu:")
            booking_id = input("> ").strip()
            if not booking_id:
                break

            if booking_id in self.bookings:
                print(f"Booking id: {booking_id}")
                selected_seats = self.bookings[booking_id]
                self.display_seats(selected_seats, booking_id)
            else:
                print(f"Booking id {booking_id} not found.")

    def display_seats(self, selected_seats=None, booking_id=None):
        row_length = len(self.seating_map[0])
        print(f"\n{' ' * (row_length // 2)} S C R E E N")
        print("-" * (row_length * 2 + 1))

        rows = len(self.seating_map)
        for i in range(rows - 1, -1, -1):
            row = []
            for j in range(len(self.seating_map[i])):
                # If booking_id is provided, mark the seats of that booking with 'o', else mark others with '#'
                if booking_id and (i, j) in selected_seats:
                    row.append('o')
                else:
                    row.append(self.seating_map[i][j])
            print(f"{chr(65 + i)} {' '.join(row)}")
        print("  ", end="")
        for i in range(len(self.seating_map[0])):
            print(i + 1, end=" ")
        print()

        # if selected_seats:
        #     print("Selected seats: ", [f"{chr(65 + r)}{c+1}" for r, c in selected_seats])

    def allocate_seats(self, num_tickets):
        selected_seats = []
        rows = len(self.seating_map)
        seats_per_row = len(self.seating_map[0])

        row_pointer = 0  # Start from the last row
        col_pointer = seats_per_row // 2 - num_tickets // 2  # Start in the middle of the row

        while num_tickets > 0:
            available_seats = []
            for row in range(rows):
                for col in range(seats_per_row):
                    if self.seating_map[row][col] == '.':
                        available_seats.append((row, col))

            if len(available_seats) == 0:
                raise ValueError("No more seats available.")

            # Check if there's enough space in the current row
            count = 0
            for r, c in available_seats:
                if r == row_pointer:
                    count += 1

            if num_tickets <= count:
                col_pointer = seats_per_row // 2 - num_tickets // 2
                for _ in range(num_tickets):
                    while self.seating_map[row_pointer][col_pointer] != '.':
                        col_pointer += 1  # Move to the next column
                        if col_pointer >= seats_per_row:
                            col_pointer = 0
                            row_pointer += 1
                    selected_seats.append((row_pointer, col_pointer))
                    self.seating_map[row_pointer][col_pointer] = 'o'
                    num_tickets -= 1
            else:
                # Allocate all available seats in the current row
                row_available_seats = []
                for r, c in available_seats:
                    if r == row_pointer:
                        row_available_seats.append((r, c))

                for r, c in row_available_seats:
                    selected_seats.append((r, c))
                    self.seating_map[r][c] = 'o'
                    num_tickets -= 1

            row_pointer += 1  # Move to the next row if needed

        return selected_seats

    def relocate_seats(self, new_position, num_tickets):
        booking_id = f"GIC{self.booking_id_counter - 1:04d}"
        previous_seats = self.bookings[booking_id]

        row_letter = new_position[0]
        start_col = int(new_position[1:]) - 1  # Convert to zero-indexed
        row = ord(row_letter.upper()) - 65  # Convert row letter to index
        rows = len(self.seating_map)
        seats_per_row = len(self.seating_map[0])

        # Mark previous seats as available '.' before relocating
        for r, c in previous_seats:
            self.seating_map[r][c] = '.'

        new_seats = []
        remaining_tickets = num_tickets
        row_pointer = row
        col_pointer = start_col

        while remaining_tickets > 0:
            available_seats = []
            for r in range(rows):
                for c in range(seats_per_row):
                    if self.seating_map[r][c] == '.':
                        available_seats.append((r, c))

            if not available_seats:
                print("Seats are not available. Keeping previous selection.")
                return previous_seats

            # Try to allocate seats to the right first
            while col_pointer < seats_per_row and remaining_tickets > 0:
                if self.seating_map[row_pointer][col_pointer] == '.':
                    new_seats.append((row_pointer, col_pointer))
                    self.seating_map[row_pointer][col_pointer] = 'o'
                    remaining_tickets -= 1
                col_pointer += 1

            # If tickets are still remaining, move to the next row and start from the middle
            if remaining_tickets > 0:
                row_pointer += 1  # Move to the next row
                if row_pointer >= rows:
                    print("No more rows available. Keeping previous selection.")
                    return previous_seats

                col_pointer = seats_per_row // 2 - remaining_tickets // 2
                while col_pointer < seats_per_row and remaining_tickets > 0:
                    if self.seating_map[row_pointer][col_pointer] == '.':
                        new_seats.append((row_pointer, col_pointer))
                        self.seating_map[row_pointer][col_pointer] = 'o'
                        remaining_tickets -= 1
                    col_pointer += 1

        self.display_seats(new_seats)

        while True:
            print("\nEnter blank to accept seat selection, or enter new seating position:")
            confirm = input("> ").strip()

            if not confirm:
                for r, c in new_seats:
                    self.seating_map[r][c] = '#'
                print("\nSeats confirmed.")
                return new_seats
            else:
                return self.relocate_seats(confirm, num_tickets)


if __name__ == "__main__":
    cinema_system = CinemaBookingSystem()
    cinema_system.start()
