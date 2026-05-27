//D:\helan\MCA_PROJECT_2\frontend\src\utils\pdfGenerator.js
import jsPDF from "jspdf";

export function downloadQuestionsAsPDF(questions) {
  const doc = new jsPDF();
  let y = 15;

  doc.setFontSize(16);
  doc.text("AI Generated Question Paper", 14, y);
  y += 10;

  doc.setFontSize(11);

  questions.forEach((q, index) => {
    if (y > 270) {
      doc.addPage();
      y = 15;
    }

    doc.text(`${index + 1}. ${q.question}`, 14, y);
    y += 7;

    if (q.options?.length) {
      q.options.forEach((opt, i) => {
        doc.text(`   ${String.fromCharCode(65 + i)}. ${opt}`, 16, y);
        y += 6;
      });
    }

    doc.text(`Bloom: ${q.bloom}`, 14, y);
    y += 5;
    doc.text(`Difficulty: ${q.difficulty}`, 14, y);
    y += 8;
  });

  doc.save("question-paper.pdf");
}