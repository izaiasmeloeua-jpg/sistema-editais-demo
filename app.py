const express = require("express");
const multer = require("multer");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

// =========================
// MULTER CONFIG (MEMÓRIA)
// =========================
const storage = multer.memoryStorage();
const upload = multer({ storage });

// =========================
// ROTA TESTE
// =========================
app.get("/", (req, res) => {
  res.json({
    status: "ok",
    message: "API de análise de editais rodando 🚀",
    endpoints: ["/upload"]
  });
});

// =========================
// 🔥 ROTA PRINCIPAL (MULTI PDF)
// =========================
app.post("/upload", upload.array("file", 50), async (req, res) => {
  try {
    const files = req.files;

    if (!files || files.length === 0) {
      return res.status(400).json({
        erro: "Nenhum arquivo enviado"
      });
    }

    // =========================
    // DEBUG LOG
    // =========================
    console.log("Arquivos recebidos:");
    files.forEach((f, i) => {
      console.log(`${i + 1} - ${f.originalname}`);
    });

    // =========================
    // (SIMULAÇÃO TEMPORÁRIA)
    // =========================
    const nomesArquivos = files.map(f => f.originalname);

    // Aqui depois entra:
    // OCR + Gemini + Airtable + Score

    return res.json({
      status: "ok",
      total_arquivos: files.length,
      arquivos: nomesArquivos,
      mensagem: "Arquivos recebidos com sucesso 🚀"
    });

  } catch (error) {
    console.error("Erro no upload:", error);

    return res.status(500).json({
      erro: "Erro ao processar upload",
      detalhe: error.message
    });
  }
});

// =========================
// PORTA
// =========================
const PORT = process.env.PORT || 8080;

app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});
