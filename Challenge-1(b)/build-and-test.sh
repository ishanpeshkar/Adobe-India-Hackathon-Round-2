#!/bin/bash

# Adobe India Hackathon 2025 - Build and Test Script
# This script helps build and test Challenge 1B solution

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}Adobe India Hackathon 2025 - Build and Test Script${NC}"
echo -e "${CYAN}====================================================${NC}"

# Function to build Challenge 1B
build_challenge_1b() {
    echo ""
    echo -e "${BLUE}Building Challenge 1B - Document Intelligence${NC}"
    echo -e "${BLUE}-----------------------------------------------${NC}"
    
    cd Challenge_1b
    
    echo "Building Docker image..."
    docker build --platform linux/amd64 -t challenge1b-processor .
    
    echo -e "${GREEN}Challenge 1B build complete!${NC}"
    cd ..
}

# Function to test Challenge 1B
test_challenge_1b() {
    echo ""
    echo -e "${YELLOW}Testing Challenge 1B${NC}"
    echo -e "${YELLOW}----------------------${NC}"
    
    cd Challenge_1b
    
    echo "Running Challenge 1B container..."
    docker run --rm challenge1b-processor
    
    echo -e "${GREEN}Challenge 1B test complete!${NC}"
    echo "Output files generated in Collection directories:"
    echo "  - Collection 1/challenge1b_output.json"
    echo "  - Collection 2/challenge1b_output.json" 
    echo "  - Collection 3/challenge1b_output.json"
    cd ..
}

# Function to validate schema
validate_schema() {
    echo ""
    echo -e "${CYAN}Validating Schema Compliance${NC}"
    echo -e "${CYAN}------------------------------${NC}"
    
    echo "Validating Challenge 1B..."
    cd Challenge_1b
    if [ -f "validate_schema.py" ]; then
        python validate_schema.py
    else
        echo -e "${YELLOW}Challenge 1B schema validation script not found${NC}"
    fi
    cd ..
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  1b-build    Build Challenge 1B Docker image"
    echo "  1b-test     Test Challenge 1B (builds if needed)"
    echo "  build       Build Challenge 1B"
    echo "  test        Test Challenge 1B"
    echo "  validate    Validate output schema"
    echo "  full        Build, test, and validate everything"
    echo "  clean       Clean up Docker images"
    echo "  help        Show this help message"
}

# Function to clean up
clean_images() {
    echo ""
    echo -e "${RED}Cleaning up Docker images${NC}"
    echo -e "${RED}---------------------------${NC}"
    
    echo "Removing Docker images..."
    docker rmi challenge1b-processor 2>/dev/null || echo "challenge1b-processor not found"
    
    echo -e "${GREEN}Cleanup complete!${NC}"
}

# Main execution
case "${1:-help}" in
    "1b-build"|"build")
        build_challenge_1b
        ;;
    "1b-test"|"test")
        build_challenge_1b
        test_challenge_1b
        ;;
    "validate")
        validate_schema
        ;;
    "full")
        build_challenge_1b
        test_challenge_1b
        validate_schema
        ;;
    "clean")
        clean_images
        ;;
    "help"|*)
        show_usage
        ;;
esac

echo ""
echo -e "${CYAN}Ready for the Adobe India Hackathon 2025!${NC}"
echo -e "${CYAN}=============================================${NC}"
