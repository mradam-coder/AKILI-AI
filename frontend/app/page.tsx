"use client";

import { useEffect, useState } from "react";
import API from "../lib/api";

// ✅ Types (important for TSX)
type Question = {
  id: number;
  question: string;
};

type Result = {
  correct: boolean;
  explanation?: string;
};

export default function Home() {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answer, setAnswer] = useState<string>("");
  const [result, setResult] = useState<Result | null>(null);

  // ✅ Fetch questions on load
  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const res = await API.get<Question[]>("/questions/");
        setQuestions(res.data);
      } catch (err: any) {
        console.error(err);
      }
    };

    fetchQuestions();
  }, []);

  // ✅ Submit answer
  const submitAnswer = async () => {
    if (questions.length === 0) return;

    try {
      const res = await API.post("/quiz/", {
        student_id: 1,
        question_id: questions[0].id,
        answer: answer,
      });

      setResult(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  // ✅ Get AI explanation
  const getExplanation = async () => {
    if (questions.length === 0) return;

    try {
      const res = await API.post("/explain/", {
        question: questions[0].question,
      });
      alert(res.data.explanation);
    } catch (err) {
      console.error("Failed to get explanation", err);
      alert("Failed to get AI explanation. Check console.");
    }
  };

  return (
    <div className="p-5">
      <h1 className="text-xl font-bold">AKILI AI LEARNING</h1>

      {/* ✅ Show question */}
      {questions.length > 0 && (
        <>
          <h2 className="mt-4">{questions[0].question}</h2>

          <input
            className="border p-2 mt-2 w-full"
            placeholder="Your answer"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
          />

          <button
            className="bg-blue-500 text-white px-4 py-2 mt-2"
            onClick={submitAnswer}
          >
            Submit
          </button>

          {/* ✅ AI Explanation Button */}
          <button
            className="bg-green-500 text-white px-4 py-2 mt-2 ml-2"
            onClick={getExplanation}
          >
            Explain with AI
          </button>
        </>
      )}

      {/* ✅ Show result */}
      {result && (
        <div className="mt-4">
          {result.correct ? (
            <p className="text-green-600">Correct ✅</p>
          ) : (
            <p className="text-red-600">
              {result.explanation || "Incorrect ❌"}
            </p>
          )}
        </div>
      )}
    </div>
  );
}