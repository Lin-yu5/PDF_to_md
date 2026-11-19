# PDF 轉 Markdown 工具 (本地離線與隱私優先)

[English](README.md) | [繁體中文](README_zh.md)

輕量、高效能且注重隱私的本地端工具，可將 PDF 文件轉換為乾淨、適合大型語言模型 (LLM) 處理的 GitHub 風格 Markdown (GFM)。

專為處理機密/敏感文件之個人、研究人員與企業打造——具備 **100% 本地離線執行**、**0 雲端 API 成本**，以及 **Windows 右鍵選單原生整合**。

---

## 核心亮點

- **100% 本地端執行，保護資料隱私**：文件完全不離開您的電腦，無遙測、不發送外部網路請求，零資料外洩風險。
- **零 API 費用**：無需申請或填入 OpenAI、Anthropic 或其他雲端 Vision API 金鑰，版面分析與 OCR 辨識完全在本機離線執行。
- **自動離線 OCR 辨識**：掃描件與純圖片型 PDF 會透過本機 RapidOCR (ONNX 執行階段) 自動進行光學文字辨識。
- **適合 LLM 的結構化 Markdown**：精準保留標題階層 (`#`, `##`, `###`)、表格 (`| 欄位1 | 欄位2 |`)、程式碼區塊、項目清單與多欄閱讀排版順序。
- **Windows 右鍵選單整合**：在 Windows 檔案總管的任何 PDF 上點選右鍵，即可一鍵完成轉換 (`轉換為 Markdown (.md)`)。
- **靈活的命令列 (CLI) 與 VS Code 支援**：支援單檔轉換、自訂輸出路徑、批次處理，並已配置 VS Code 一鍵轉換建置工作。

---

## 系統架構與轉換引擎比較

| 功能特性 | 本專案 (PyMuPDF4LLM + RapidOCR) | 雲端多模態 API (如 GPT-4o) | 傳統 PDF 提取工具 (如 pypdf) |
| :--- | :--- | :--- | :--- |
| **隱私與安全性** | **100% 本地離線** | 需將文件上傳至雲端伺服器 | 本地端 |
| **使用成本** | **$0.00 (完全免費)** | 按 Token / 圖片張數計費 (累積昂貴) | $0.00 |
| **掃描件 OCR** | **內建本地 ONNX OCR** | 支援 (費用高昂) | 通常無法辨識或回傳空白 |
| **表格解析** | **標準 Markdown 管道表格** | Markdown 表格 | 壓平為無結構的純文字 |
| **標題階層辨識** | **字體大小與字重分析** | 模型推論 | 純文字 |
| **轉換速度** | **毫秒級 (~0.7 秒)** | 3~10 秒網路往返延遲 | 快速 |

---

## 安裝指南

### 前置需求
- Python 3.10 或更高版本
- Windows 10/11（支援右鍵選單功能；命令列介面支援跨平台 macOS/Linux）

### 安裝步驟
1. 複製 (Clone) 或下載此專案：
   ```bash
   git clone https://github.com/your-username/pdf-to-md.git
   cd pdf-to-md
   ```

2. 安裝必要依賴套件：
   ```bash
   pip install -r requirements.txt
   ```

---

## Windows 右鍵選單設定 (檔案總管整合)

在 Windows 檔案總管中，對任何 PDF 按右鍵即可直接轉換：

### 1-鍵快速安裝
在專案目錄下雙擊 `install_context_menu.bat`，或在終端機執行：
```bash
python setup_context_menu.py --install
```

- **免系統管理員權限**：註冊於目前使用者的登錄檔路徑 `HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\.pdf`。
- **背景無感靜默執行**：使用 `pythonw.exe` 執行，螢幕不會閃爍彈出黑色的命令提示字元視窗。
- **自動產出同目錄**：直接在該 PDF 的同目錄下生成 `<檔案名稱>.md`。

### 解除安裝
雙擊 `uninstall_context_menu.bat`，或執行：
```bash
python setup_context_menu.py --uninstall
```

---

## 命令列 (CLI) 使用說明

### 1. 基本轉換
將 PDF 轉換為同目錄下的 Markdown (`document.pdf` -> `document.md`)：
```bash
python pdf_to_md.py document.pdf
```

### 2. 指定輸出檔案路徑
指定目標 Markdown 檔案路徑：
```bash
python pdf_to_md.py document.pdf output.md
# 或使用 -o 參數：
python pdf_to_md.py -o /path/to/custom_output.md document.pdf
```

### 3. 批次轉換
一次轉換多個 PDF 檔案：
```bash
python pdf_to_md.py report1.pdf report2.pdf thesis.pdf
```

### 4. 提取嵌入圖片
將 PDF 中的圖片擷取並存放在專屬資料夾中：
```bash
python pdf_to_md.py --extract-images report.pdf
```

### 5. CLI 參數一覽

```text
usage: pdf_to_md.py [-h] [-o OUTPUT] [--engine {auto,pymupdf4llm,markitdown}]
                    [--extract-images] [-v] [-q] [--version]
                    [inputs ...]

positional arguments:
  inputs                輸入的 PDF 檔案路徑 (可為多個)

options:
  -h, --help            顯示說明訊息並退出
  -o, --output OUTPUT   指定輸出 Markdown 檔案路徑 (單檔模式)
  --engine {auto,pymupdf4llm,markitdown}
                        指定轉換引擎 (預設 auto: 優先使用 pymupdf4llm)
  --extract-images      提取並儲存 PDF 內嵌圖片至本地
  -v, --verbose         顯示詳細除錯記錄
  -q, --quiet           靜默模式 (僅在錯誤時輸出)
  --version             顯示程式版本
```

---

## VS Code 快捷操作

本專案已包含 `.vscode` 設定檔：
- 開啟或選取 PDF 檔案後，按下 **`Ctrl + Shift + B`** 即可在 VS Code 內一鍵轉換。
- 按下 **`F5`** 可對 `pdf_to_md.py` 進行中斷點除錯。

---

## 專案結構

```text
.
├── pdf_to_md.py                # 主轉換程式 (支援 CLI 與右鍵選單呼叫)
├── setup_context_menu.py       # 右鍵選單註冊/反註冊工具
├── install_context_menu.bat    # Windows 右鍵選單一鍵安裝批次檔
├── uninstall_context_menu.bat  # Windows 右鍵選單一鍵移除批次檔
├── add_pdf_to_md_context.reg   # 右鍵選單登錄檔模板
├── remove_pdf_to_md_context.reg# 移除右鍵選單登錄檔
├── requirements.txt            # 依賴套件清單
├── .gitignore                  # Git 忽略設定
├── LICENSE                     # MIT 開源授權條款
├── README.md                   # 英文說明文件
└── README_zh.md                # 繁體中文說明文件
```

---

## 開源授權

本專案採用 [MIT License](LICENSE) 授權條款。
