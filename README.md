# 菇得 - 後端

[SITCON Camp 2025](https://sitcon.camp/2025) 第二小隊的黑客松專案

### Running the Server

這個專案使用 [uv](https://docs.astral.sh/uv) 進行套件管理，請在安裝 uv 後，執行以下指令建構虛擬環境

```bash
uv sync
```

並在虛擬環境建立，可以在在虛擬環境內執行以下指令來啟動 dev server

```bash
fastapi dev src/main.py
```
