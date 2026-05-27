//D:\helan\MCA_PROJECT_2\frontend\src\utils\exportPdf.js
import jsPDF from "jspdf";
import "jspdf-autotable";

/**
 * Exports questions to a PDF file.
 * @param {Array} questions - The list of question objects.
 * @param {boolean} includeAnswers - Whether to include the answers in the PDF.
 */
export const exportQuestionsToPDF = (questions, includeAnswers = true) => {
  const doc = new jsPDF();
  const pageWidth = doc.internal.pageSize.getWidth();
  const margin = 14;
  const maxWidth = pageWidth - margin * 2; 
  let y = 15;

  // Title
  doc.setFontSize(16);
  doc.setFont("helvetica", "bold");
  doc.text(includeAnswers ? "Question Paper with Answers" : "Question Paper", margin, y);
  y += 12;

  questions.forEach((q, index) => {
    // Page overflow check
    if (y > 250) {
      doc.addPage();
      y = 20;
    }

    // 1. Question Text
    doc.setFontSize(12);
    doc.setFont("helvetica", "bold");
    const questionText = `Q${index + 1}. ${q.question}`;
    const wrappedQuestion = doc.splitTextToSize(questionText, maxWidth);
    doc.text(wrappedQuestion, margin, y);
    y += wrappedQuestion.length * 7;

    // 2. MCQ Options
    if (q.options && q.options.length > 0) {
      doc.setFont("helvetica", "normal");
      doc.setFontSize(11);
      q.options.forEach((opt, i) => {
        const optionText = `   ${String.fromCharCode(65 + i)}. ${opt}`;
        const wrappedOption = doc.splitTextToSize(optionText, maxWidth - 10);
        doc.text(wrappedOption, margin, y);
        y += wrappedOption.length * 6;
      });
      y += 2;
    }

    // 3. Conditional Answer Rendering
    if (includeAnswers && q.answer) {
      doc.setFontSize(11);
      doc.setFont("helvetica", "bold");
      doc.setTextColor(40, 167, 69); // Optional: Green color for answers
      const answerText = `Answer: ${q.answer}`;
      const wrappedAnswer = doc.splitTextToSize(answerText, maxWidth - 5);
      doc.text(wrappedAnswer, margin + 4, y);
      y += wrappedAnswer.length * 6 + 2;
      doc.setTextColor(0, 0, 0); // Reset to black
    }

    // 4. Meta Data
    doc.setFontSize(9);
    doc.setFont("helvetica", "italic");
    doc.setTextColor(100);
    const metaText = `Type: ${q.type} | Bloom: ${q.bloom_level || "-"} | Difficulty: ${q.difficulty || "-"}`;
    doc.text(metaText, margin + 4, y);
    doc.setTextColor(0);

    y += 15; // Spacing between questions
  });

  const fileName = includeAnswers ? "questions_with_answers.pdf" : "questions_only.pdf";
  doc.save(fileName);
};
