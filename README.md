# Multi-Vehicle Search API

A FastAPI-based service for finding optimal storage locations for multiple vehicles using advanced 2D bin packing algorithms.

## Features

- **2D Grid Packing**: Efficiently arranges vehicles in 2D space within listings
- **Smart Allocation**: Distributes vehicles across multiple listings when needed
- **Cost Optimization**: Returns results sorted by total price (ascending)
- **High Performance**: ~40ms average response time for 7000+ listings
- **Scalable**: Handles up to 5 vehicles per request

## Requirements

- Python 3.11+
- FastAPI
- Uvicorn

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Multi-Vehicle-Search
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running Locally

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Or with hot reload:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check

```bash
GET /
```

**Response:**
```json
{
  "status": "ok",
  "message": "Multi-Vehicle Search API"
}
```

### Search for Storage Locations

```bash
POST /
```

**Request Body:**
```json
[
  {
    "length": 10,
    "quantity": 1
  },
  {
    "length": 20,
    "quantity": 2
  }
]
```

**Parameters:**
- `length` (int): Vehicle length in feet
- `quantity` (int): Number of vehicles with this length
- Vehicle width is always 10 feet
- Total quantity across all items must be ≤ 5

**Response:**
```json
[
  {
    "location_id": "42b8f068-2d13-4ed1-8eec-c98f1eef0850",
    "listing_ids": ["b9bbe25f-5679-4917-bd7b-1e19c464f3a8"],
    "total_price_in_cents": 1005
  },
  {
    "location_id": "507628b8-163e-4e22-a6a3-6a16f8188928",
    "listing_ids": ["e7d59481-b804-4565-b49b-d5beb7aec350"],
    "total_price_in_cents": 1088
  }
]
```

**Response Fields:**
- `location_id`: Unique identifier for the storage location
- `listing_ids`: Array of listing IDs used for storage
- `total_price_in_cents`: Total cost in cents (sum of all listings)

**Response Characteristics:**
- Includes every location that can store all requested vehicles
- Shows the cheapest combination of listings per location
- One result per location_id
- Sorted by total_price_in_cents (ascending)

## Testing

### Test with curl

**Simple test (1 vehicle):**
```bash
curl -X POST "http://localhost:8000/" \
  -H "Content-Type: application/json" \
  -d '[{"length": 10, "quantity": 1}]'
```

**Complex test (multiple vehicles):**
```bash
curl -X POST "http://localhost:8000/" \
  -H "Content-Type: application/json" \
  -d '[
    {"length": 10, "quantity": 1},
    {"length": 20, "quantity": 2},
    {"length": 25, "quantity": 1}
  ]'
```

## Project Structure

```
Multi-Vehicle-Search/
├── main.py           # FastAPI application and endpoints
├── models.py         # Pydantic data models
├── data.py           # Data loading and caching
├── algorithm.py      # Core packing algorithms
├── listings.json     # Storage listings data (7000+ entries)
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Algorithm Design

### 1. Single Listing Packing (`can_fit_vehicles`)

Uses **backtracking with 2D grid packing**:
- Calculates available rows based on listing dimensions
- Places vehicles into rows using backtracking
- Tries both orientations (length along L or W)
- Prunes duplicate states for efficiency

### 2. Multi-Listing Allocation (`can_allocate`)

Distributes vehicles across multiple listings:
- Backtracking assigns each vehicle to a listing
- Validates each listing using `can_fit_vehicles`
- Ensures 2D packing within each individual listing

### 3. Cost Optimization (`find_cheapest_combination`)

Finds the cheapest combination per location:
- Tries single listings first (cheapest option)
- Incrementally tries combinations of 2, 3, 4, 5 listings
- Stops at first valid combination (greedy for size)
- Returns cheapest combination found

### Key Assumptions

1. **Same orientation per listing**: All vehicles in a listing face the same direction
2. **No buffer space**: Vehicles can be placed directly adjacent
3. **Vehicle width**: Fixed at 10 feet
4. **Listing dimensions**: All multiples of 10

## Deployment

### Deploy to Render

This project is configured for Render deployment. Simply connect your repository and deploy.

https://multi-vehicle-search-26gg.onrender.com

### Environment Variables

No environment variables required. The app reads `listings.json` from the local filesystem.

