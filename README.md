# vilab-3d-llm

Cấu hình model, script tải model và bộ đánh giá trợ giảng AI của **ViLab 3D**. Repo này lo phần chạy model
(Qwen qua Ollama, embedding bge-m3) và đánh giá model. RAG và system prompt nằm ở `vilab-3d-backend`.

## Hệ thống gồm

- `vilab-3d-frontend`: giao diện React + Three.js
- `vilab-3d-backend`: API FastAPI, PostgreSQL + pgvector, RAG
- `vilab-3d-assets`: file mô hình 3D `.glb`
- `vilab-3d-llm`: cấu hình model và bộ đánh giá (repo này)

## Cài model lần đầu

Cài Ollama trực tiếp từ [ollama.com](https://ollama.com), sau đó:

```bash
./scripts/pull-models.sh     # tải qwen3:8b, bge-m3 và tạo model vilab-qwen
./scripts/smoke-test.sh      # gọi thử API chuẩn OpenAI của Ollama
```

Đổi dòng `FROM` trong `models/Modelfile.qwen` (và lệnh `ollama pull` tương ứng) nếu cần bản Qwen khác
cho vừa VRAM. Trên Windows, chạy hai script bằng Git Bash.

## Đánh giá model

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python eval/eval_llm.py
```

| `EVAL_MODE` | Gọi tới | Đo gì |
|---|---|---|
| `llm` | `LLM_BASE_URL` (Ollama local, Ollama trên Kaggle hoặc Qwen API) | Khả năng của model khi không có RAG |
| `backend` | API chat của backend qua `BACKEND_URL` | Cả hệ thống khi có RAG (chưa hỗ trợ, chờ backend có API chat) |

Bộ câu hỏi nằm ở `eval/questions.jsonl` (mỗi dòng một câu: `id`, `subject`, `grade`, `question`,
`reference`). Kết quả lưu thành file CSV trong `eval/results/`.

## Cấu trúc

```
models/Modelfile.qwen     # shared model parameters
scripts/                  # pull-models.sh, smoke-test.sh
eval/                     # questions.jsonl, eval_llm.py, results/
notebooks/                # Kaggle notebooks (Giai đoạn 6)
docker-compose.yml        # Ollama on the VPS (production stage)
```
