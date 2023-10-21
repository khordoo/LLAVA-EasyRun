# LLAVA-EasyRun

**LLAVA-EasyRun** is a simplified setup for running the **LLAVA** project using Docker, designed to make it extremely easy for users to get started. It utilizes the **llama.cpp** for local CPU execution and comes with a custom, user-friendly GUI for a hassle-free interaction.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)

### Usage

1. Clone this repository to your local machine:
```bash
   git clone https://github.com/your-username/LLAVA-EasyRun.git
```
   
2. Navigate to the project directory:
  ```bash
   cd LLAVA-ReadyRun
   ```
3.Build the Docker image:
```bash
docker build -t llava-easy-run .
```
4. Start the LLAVA-ReadyRun GUI:
```bash
docker run -it -p 8501:8501 llava-easy-run
```
5. Access the GUI in your web browser at http://localhost:8501.

## Performance Considerations
Please note that running LLAVA-ReadyRun on a CPU may result in slightly reduced performance compared to GPU-based setups. However, this trade-off ensures a straightforward and accessible user experience.

## Acknowledgments
- [LLAVA](https://github.com/haotian-liu/LLaVA)

## Feedback and Contributions
Feedback, issues, and contributions are welcome. Feel free to open an issue or submit a pull request to help improve LLAVA-ReadyRun.