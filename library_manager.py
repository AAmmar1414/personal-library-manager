import streamlit as st
import json
import os

# File to save and load library data
LIBRARY_FILE = "library.txt"

# Load library from file
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# Save library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file)

# Streamlit app
def main():
    st.title("Personal Library Manager")

    # Load library
    library = load_library()

    # Sidebar menu
    menu = ["Add a book", "Remove a book", "Search for a book", "Display all books", "Display statistics"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Add a book":
        st.header("Add a Book")
        with st.form("add_book_form"):
            title = st.text_input("Enter the book title")
            author = st.text_input("Enter the author")
            year = st.number_input("Enter the publication year", min_value=0, step=1)
            genre = st.text_input("Enter the genre")
            read_status = st.radio("Have you read this book?", ("Yes", "No"))
            submitted = st.form_submit_button("Add Book")

            if submitted:
                library.append({
                    "title": title,
                    "author": author,
                    "year": int(year),
                    "genre": genre,
                    "read": read_status == "Yes",
                })
                save_library(library)
                st.success("Book added successfully!")

    elif choice == "Remove a book":
        st.header("Remove a Book")
        title = st.text_input("Enter the title of the book to remove")
        if st.button("Remove Book"):
            for book in library:
                if book["title"].lower() == title.lower():
                    library.remove(book)
                    save_library(library)
                    st.success("Book removed successfully!")
                    break
            else:
                st.error("Book not found.")

    elif choice == "Search for a book":
        st.header("Search for a Book")
        search_by = st.radio("Search by", ("Title", "Author"))
        query = st.text_input("Enter the search term")
        if st.button("Search"):
            matches = [
                book for book in library
                if (search_by == "Title" and query.lower() in book["title"].lower()) or
                   (search_by == "Author" and query.lower() in book["author"].lower())
            ]
            if matches:
                st.subheader("Matching Books:")
                for book in matches:
                    read_status = "Read" if book["read"] else "Unread"
                    st.write(f"- {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
            else:
                st.warning("No matching books found.")

    elif choice == "Display all books":
        st.header("Display All Books")
        if library:
            for book in library:
                read_status = "Read" if book["read"] else "Unread"
                st.write(f"- {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
        else:
            st.info("Your library is empty.")

    elif choice == "Display statistics":
        st.header("Library Statistics")
        total_books = len(library)
        if total_books > 0:
            read_books = sum(1 for book in library if book["read"])
            percentage_read = (read_books / total_books) * 100
            st.write(f"Total books: {total_books}")
            st.write(f"Percentage read: {percentage_read:.1f}%")
        else:
            st.info("No books in the library to calculate statistics.")

if __name__ == "__main__":
    main()
