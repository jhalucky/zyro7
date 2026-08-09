# Model Benchmarks

## Hardware

- CPU: Intel Core i5-1335U
- CPU cores: 10
- CPU threads: 12
- Linux RAM: ~8 GB
- GPU: None

## Qwen2.5-Coder 7B

- Ollama model size: ~4.7 GB
- CPU-only
- Context: 4096
- Initial simple prompt: ~127 seconds
- Conclusion: Too heavy for our 8 GB Linux environment

## Qwen2.5-Coder 3B

- Ollama model size: ~1.9 GB
- Loaded size: ~2.2 GB
- CPU-only
- Context: 4096
- Simple provider request: ~1.9 seconds
- Conclusion: Suitable for local development

## Decision

Use Qwen2.5-Coder 3B as the local development model.

Keep the model provider abstraction independent of Ollama so that stronger remote models can be introduced later.