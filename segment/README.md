# Image Analysis and Ingredient Detection Project

This project combines Computer Vision and Large Language Models (LLMs) to analyze images, detect objects, and identify ingredients. It uses Python to implement a sophisticated image processing pipeline with an interactive user interface.

## Features and Rationale

1. **LLM + Computer Vision Integration**
   - *Why*: Combining LLMs with CV allows for more intelligent and context-aware image analysis, going beyond simple object detection.
   - *How*: Utilizes Python to integrate LLM capabilities with computer vision techniques.

2. **Object Detection with Meta Segment Anything Model (SAM)**
   - *Why*: SAM provides state-of-the-art segmentation, allowing for precise object identification in complex images.
   - *How*: Uses SAM to identify and segment objects in input images.

3. **Adaptive Segmentation**
   - *Why*: Ensures accurate detection in images with varying levels of detail or complexity.
   - *How*: If too many objects are detected in one segment, the LLM instructs SAM to perform finer-grained segmentation (e.g., from 40px x 40px to 10px x 10px).

4. **Object Labeling**
   - *Why*: Provides a clear, numerical reference for each detected object without relying on predefined categories.
   - *How*: Assigns numerical labels to all detected objects, similar to YOLO but using index numbers instead of predefined class names.

5. **Ingredient Identification with LLM**
   - *Why*: Leverages the power of LLMs to identify ingredients and their relationships, providing context beyond simple object detection.
   - *How*: Employs an LLM to identify ingredients in each segment and establishes relationships between segments.

6. **Web Search Integration**
   - *Why*: Enhances the accuracy of ingredient identification by cross-referencing with online sources when LLM results are unclear.
   - *How*: Performs a Google image search and summarizes findings when LLM results are ambiguous.

7. **Interactive UI**
   - *Why*: Provides a user-friendly way to visualize and interact with the analyzed image and its components.
   - *How*: Displays segmented images with highlighted frames, allowing users to loop through segments and view ingredient information.

8. **Ingredient Query**
   - *Why*: Enables quick lookup of specific ingredients within the analyzed image.
   - *How*: Allows users to search for specific ingredients, highlighting the corresponding segment and displaying its index.

## Critical User Journey

1. **Image Input**: User uploads an image of a complex scene (e.g., a kitchen counter with various ingredients).

2. **Initial Segmentation**: The system uses SAM to segment the image into distinct objects.

3. **Adaptive Refinement**: If certain areas are too complex, the LLM requests finer segmentation from SAM.

4. **Object Labeling**: Each identified segment is assigned a unique numerical index.

5. **Ingredient Analysis**: The LLM analyzes each segment to identify potential ingredients.

6. **Web Search Verification**: For ambiguous items, the system performs a web search to confirm or clarify the LLM's analysis.

7. **Results Display**: The UI presents the segmented image with numbered labels.

8. **Interactive Exploration**: 
   - User can cycle through each segment, with the system highlighting the current segment and providing ingredient information.
   - User can query specific ingredients, and the system highlights the relevant segment(s).

9. **Refinement and Learning**: Based on user feedback, the system can adjust its analysis, improving accuracy over time.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/image-ingredient-analyzer.git

# Navigate to the project directory
cd image-ingredient-analyzer

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install required packages
pip install -r requirements.txt
```

## Usage

```bash
# Run the main application
python main.py --image path/to/your/image.jpg
```

For more detailed usage instructions, refer to the [User Guide](docs/USER_GUIDE.md).

## Dependencies

- Python 3.8+
- PyTorch 1.9+
- torchvision
- Segment Anything Model (SAM)
- Transformers (for LLM integration)
- OpenCV
- Flask (for web UI)

For a complete list of dependencies, see the `requirements.txt` file.