# Traveling Salesman Problem (TSP) Streamlit Application

This project implements a web application using Streamlit to solve the Traveling Salesman Problem (TSP) using two algorithms: Brute Force and Genetic Algorithm. Users can select an algorithm to visualize the best tour and its total distance.

## Project Structure

```
tsp_streamlit_app
├── src
│   ├── main.py                # Main logic for running the algorithms
│   ├── streamlit_app.py       # Entry point for the Streamlit web application
│   ├── algorithms
│   │   ├── __init__.py        # Initializes the algorithms package
│   │   ├── brute.py           # Implementation of the brute force algorithm
│   │   └── ga.py              # Implementation of the genetic algorithm
│   └── utils
│       └── plot.py            # Functions for plotting the results
├── requirements.txt           # Lists project dependencies
└── README.md                  # Documentation for the project
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd tsp_streamlit_app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

To run the Streamlit application, execute the following command in your terminal:
```
streamlit run src/streamlit_app.py
```

## Usage

- Once the application is running, you can select either the Brute Force or Genetic Algorithm from the dropdown menu.
- After selecting an algorithm, click the "Run" button to generate the cities and compute the best tour.
- The application will display the best tour and its total distance, along with a visualization of the cities and the tour.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License.