const express = require("express");
const multer = require("multer");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

// =========================
// CONFIG MULTER (MEMÓRIA)
// =========================
const storage = multer.memoryStorage();

const upload = multer({
  storage: storage,
  limits: { fileSize: 20 * 1024 * 1024 } // 20MB por arquivo
});

// =========================
// ROTA TESTE
// =========================
app.get("/", (req, res) => {
  res.json({
    status: "ok",
    message: "API rodando 🚀"
  });
});

// =========================
// ROTA UPLOAD (MULTI)
// =========================
app.post("/upload", upload.array("file", 50), async (req, res) => {
  try {
    const arquivos = req.files;

    if (!arquivos || arquivos.length === 0) {
      return res.status(400).json({
        erro: "Nenhum arquivo enviado"
      });
    }

    console.log("Arquivos recebidos:");
    arquivos.forEach((f, i) => {
      console.log(`${i + 1} - ${f.originalname}`);
    });

    // =========================
    // IDENTIFICAÇÃO SIMPLES
    // =========================
    let edital = null;
    let tr = null;
    let anexos = [];

    arquivos.forEach(file => {
      const nome = file.originalname.toLowerCase();

      if (nome.includes("edital") && !edital) {
        edital = file;
      } else if (
        nome.includes("termo") ||
        nome.includes("referencia") ||
        nome.includes("tr")
      ) {
        tr = file;
      } else {
        anexos.push(file);
      }
    });

    // =========================
    // RESPOSTA
    // =========================
    return res.json({
      status: "ok",
      total_arquivos: arquivos.length,
      edital: edital ? edital.originalname : null,
      termo_referencia: tr ? tr.originalname : null,
      anexos: anexos.map(a => a.originalname)
    });

  } catch (error) {
    console.error("Erro no upload:", error);

    return res.status(500).json({
      erro: "Erro interno",
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
