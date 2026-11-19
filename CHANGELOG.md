# 更新紀錄 (Changelog)

所有本專案的重大變更與版本更新皆記錄於此文件。

---

## [v1.1.0] - 2026-11-19

### 🎯 重點更新摘要
透過實測 94 頁醫療混合型投影片（`CP.pdf`），大幅增強圖文混合型 PDF 的 OCR 擷取完整度、排版結構與閱讀品質。

### ✨ 新增功能 (Features)
- **`--force-ocr` 參數**：
  - 強制對全文件所有頁面及內嵌圖片進行深度 OCR 辨識。
  - 解決原本版面評估器門檻（0.93）過高導致「少文字標題 + 大掃描表格」被誤判為純圖片而漏失文字的問題。
- **`--page-separators` 參數**：
  - 在輸出 Markdown 中自動插入簡報換頁分隔線與標記（`--- \n*Page N*\n`），方便精準定位每一張 Slide。

### 🛠️ 優化與修復 (Bug Fixes & Refinements)
- **OCR 假刪除線清洗（`clean_markdown_output`）**：
  - 修復掃描文件格線穿過文字時被誤判為 `strikethrough`（刪除線 `~~`）的雜訊，自動還原斷詞（例如：`protect ~~i~~ veresponses` $\rightarrow$ `protectiveresponses`）。
- **文件與環境配置同步**：
  - 更新 `README.md` 與 `README_zh.md`，納入最新參數說明與 CLI 語法範例。
  - 更新 `.gitignore`。

### 📊 實測成效 (Benchmark on CP.pdf)
- **Markdown 總字數**：45,377 字 $\rightarrow$ **55,603 字**（+10,226 字原本被略過的醫學圖表內容）。
- **分頁精度**：94 頁 100% 精準標記。
