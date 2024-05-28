import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
    const [initialQuestions, setInitialQuestions] = useState([
        "What is your first and last name?",
        "What is your approximate height?",
        "What is your approximate weight?",
        "Are you currently taking any medications?",
        "Have you had any recent surgeries?",
        "Do you have any known drug allergies?",
        "Finally, could you tell me what your going into the office for?",
    ]);
    const [chatHistory, setChatHistory] = useState([]);
    const [userMessage, setUserMessage] = useState("");
    const [isConversationStarted, setIsConversationStarted] = useState(false);
    const [isConversationFinished, setIsConversationFinished] = useState(false);
    const [stageNumber, setStageNumber] = useState(0);
    const [height, setHeight] = useState("4'0\"");

    const handleInitialQuestionsChange = (e) => {
        setInitialQuestions({
            ...initialQuestions,
            [e.target.name]: e.target.value,
        });
    };

    const handleInitialQuestionsChangeYN = (answer) => {
        setInitialQuestions({
            ...initialQuestions,
            [initialQuestions[stageNumber - 1]]: answer,
        });
    };

    const startConversation = async () => {
        try {
            const response = await axios.post(
                "http://127.0.0.1:5000/start",
                initialQuestions,
                {
                    headers: { "Content-Type": "application/json" },
                }
            );
            setChatHistory([
                { role: "assistant", content: response.data.initial_response },
            ]);
            setIsConversationStarted(true);
        } catch (error) {
            console.error("Error starting conversation:", error);
        }
    };

    const sendMessage = async () => {
        try {
            const response = await axios.post(
                "http://127.0.0.1:5000/chat",
                { message: userMessage },
                {
                    headers: { "Content-Type": "application/json" },
                }
            );
            setChatHistory([
                ...chatHistory,
                { role: "user", content: userMessage },
                { role: "assistant", content: response.data.response },
            ]);
            setUserMessage("");
            if (response.data.finished) {
                setIsConversationFinished(true);
            }
        } catch (error) {
            console.error("Error sending message:", error);
        }
    };

    const fetchReport = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:5000/report");
            console.log("Report:", response.data);
        } catch (error) {
            console.error("Error fetching report:", error);
        }
    };

    return (
        <div
            style={{
                display: "flex",
                width: "100vw",
                height: "100vh",
                textAlign: "center",
                fontFamily: "Tahoma",
                justifyContent: "center",
                background:
                    "linear-gradient(165deg, hsl(202deg 100% 50%) 0%, hsl(203deg 100% 58%) 7%,hsl(203deg 100% 62%) 14%,hsl(203deg 100% 65%) 19%,hsl(203deg 100% 69%) 24%,hsl(202deg 100% 72%) 29%,hsl(202deg 100% 75%) 32%,hsl(203deg 100% 80%) 36%,hsl(203deg 100% 85%) 40%,hsl(204deg 100% 89%) 44%,hsl(205deg 100% 93%) 52%,hsl(205deg 100% 96%) 66%,hsl(0deg 0% 100%) 100%)",
                color: "black",
            }}
        >
            {!isConversationStarted ? (
                (stageNumber === 0 && (
                    <div
                        style={{
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            flexDirection: "column",
                        }}
                    >
                        <div
                            style={{
                                height: "30%",
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: "column",
                            }}
                        >
                            <img
                                src="\Time-Machine.svg"
                                alt="time"
                                style={{ width: "50px" }}
                            ></img>
                        </div>
                        <div
                            style={{
                                height: "30%",
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: "column",
                            }}
                        >
                            <p
                                style={{
                                    fontSize: "28px",
                                    fontWeight: "500",
                                    marginBottom: "0px",
                                }}
                            >
                                Reduce your wait time
                            </p>
                            <p>
                                Take a few moments to complete your Breezy
                                assessment.
                            </p>
                        </div>
                        <div
                            style={{
                                height: "30%",
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: "column",
                            }}
                        >
                            <button
                                style={{
                                    backgroundColor: "#00A3FF",
                                    border: "none",
                                    color: "white",
                                    padding: "10px",
                                    borderRadius: "20px",
                                    cursor: "pointer",
                                }}
                                onClick={() => {
                                    setStageNumber(stageNumber + 1);
                                }}
                            >
                                Begin your assessment
                            </button>
                        </div>
                    </div>
                )) ||
                (stageNumber === 1 && (
                    <div
                        style={{
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            flexDirection: "column",
                            width: "60%",
                        }}
                    >
                        <div
                            style={{
                                height: "30%",
                                width: "100%",
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center",
                                flexDirection: "row",
                            }}
                        >
                            <p
                                style={{ cursor: "pointer", fontSize: "20px" }}
                                onClick={() => {
                                    setStageNumber(stageNumber - 1);
                                }}
                            >
                                &lt; Previous
                            </p>
                            <img
                                style={{ width: "40px" }}
                                src="./Logo.svg"
                                alt="Logo"
                            />
                        </div>
                        <div
                            style={{
                                height: "30%",
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: "column",
                            }}
                        >
                            <p style={{ fontSize: "24px" }}>
                                Welcome. I’m Ava, your virtual Nurse.
                            </p>
                            <p>
                                Let's get started.{" "}
                                {initialQuestions[stageNumber - 1]}
                            </p>
                        </div>
                        <div
                            style={{
                                height: "30%",
                                width: "100%",
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: "column",
                            }}
                        >
                            <input
                                style={{
                                    borderColor: "#00A3FF",
                                    borderRadius: "30px",
                                    textAlign: "center",
                                    color: "#00A3FF",
                                    marginBottom: "10px",
                                    width: "12em",
                                    height: "1.5em",
                                }}
                                type="text"
                                placeholder="e.g. John Smith"
                                name={initialQuestions[stageNumber - 1]}
                                onChange={handleInitialQuestionsChange}
                            />
                            <button
                                style={{
                                    border: "none",
                                    backgroundColor: "transparent",
                                    cursor: "pointer",
                                }}
                                onClick={() => {
                                    setStageNumber(stageNumber + 1);
                                }}
                            >
                                Continue &gt;
                            </button>
                        </div>
                    </div>
                )) ||
                (stageNumber === 2 && (
                    <div
                        style={{
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            flexDirection: "column",
                            width: "60%",
                        }}
                    >
                        <div
                            style={{
                                height: "30%",
                                width: "100%",
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center",
                                flexDirection: "row",
                            }}
                        >
                            <p
                                style={{ cursor: "pointer", fontSize: "20px" }}
                                onClick={() => {
                                    setStageNumber(stageNumber - 1);
                                }}
                            >
                                &lt; Previous
                            </p>
                            <img
                                style={{ width: "40px" }}
                                src="./Logo.svg"
                                alt="Logo"
                            />
                        </div>
                        <div
                            style={{
                                height: "30%",
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: "column",
                            }}
                        >
                            <p>{initialQuestions[stageNumber - 1]}</p>
                        </div>
                        <div
                            style={{
                                height: "30%",
                                width: "100%",
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: "column",
                            }}
                        >
                            <div>{height}</div>
                            <input
                                style={{
                                    borderColor: "#00A3FF",
                                    borderRadius: "30px",
                                    textAlign: "center",
                                    color: "#00A3FF",
                                    marginBottom: "10px",
                                    width: "12em",
                                    height: "1.5em",
                                }}
                                type="range"
                                min="48"
                                max="84"
                                name="height"
                                onChange={(event) => {
                                    const inches = event.target.value;
                                    const feet = Math.floor(inches / 12);
                                    const remainingInches = inches % 12;
                                    const newHeight = `${feet}'${remainingInches}"`;
                                    setHeight(newHeight);
                                    handleInitialQuestionsChange({
                                        target: {
                                            name: "height",
                                            value: newHeight,
                                        },
                                    });
                                }}
                            />
                            <button
                                style={{
                                    border: "none",
                                    backgroundColor: "transparent",
                                    cursor: "pointer",
                                }}
                                onClick={() => {
                                    setStageNumber(stageNumber + 1);
                                }}
                            >
                                Continue &gt;
                            </button>
                        </div>
                    </div>
                )) ||
                (stageNumber === 3 && (
                    <div
                        style={{
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            flexDirection: "column",
                            width: "60%",
                        }}
                    >
                        <div
                            style={{
                                height: "30%",
                                width: "100%",
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center",
                                flexDirection: "row",
                            }}
                        >
                            <p
                                style={{ cursor: "pointer", fontSize: "20px" }}
                                onClick={() => {
                                    setStageNumber(stageNumber - 1);
                                }}
                            >
                                &lt; Previous
                            </p>
                            <img
                                style={{ width: "40px" }}
                                src="./Logo.svg"
                                alt="Logo"
                            />
                        </div>
                        <div
                            style={{
                                height: "30%",
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: "column",
                            }}
                        >
                            <p>{initialQuestions[stageNumber - 1]}</p>
                        </div>
                        <div
                            style={{
                                height: "30%",
                                width: "100%",
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: "column",
                            }}
                        >
                            <input
                                style={{
                                    borderColor: "#00A3FF",
                                    borderRadius: "30px",
                                    textAlign: "center",
                                    color: "#00A3FF",
                                    marginBottom: "10px",
                                    width: "12em",
                                    height: "1.5em",
                                }}
                                type="text"
                                placeholder="e.g. 50 lb or 23 kg"
                                name={initialQuestions[stageNumber - 1]}
                                onChange={handleInitialQuestionsChange}
                            />
                            <button
                                style={{
                                    border: "none",
                                    backgroundColor: "transparent",
                                    cursor: "pointer",
                                }}
                                onClick={() => {
                                    setStageNumber(stageNumber + 1);
                                }}
                            >
                                Continue &gt;
                            </button>
                        </div>
                    </div>
                )) ||
                (stageNumber === 4 && (
                    <div
                        style={{
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            flexDirection: "column",
                            width: "60%",
                        }}
                    >
                        <div
                            style={{
                                height: "30%",
                                width: "100%",
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center",
                                flexDirection: "row",
                            }}
                        >
                            <p
                                style={{ cursor: "pointer", fontSize: "20px" }}
                                onClick={() => {
                                    setStageNumber(stageNumber - 1);
                                }}
                            >
                                &lt; Previous
                            </p>
                            <img
                                style={{ width: "40px" }}
                                src="./Logo.svg"
                                alt="Logo"
                            />
                        </div>
                        <div
                            style={{
                                height: "30%",
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: "column",
                            }}
                        >
                            <p>{initialQuestions[stageNumber - 1]}</p>
                        </div>
                        <div
                            style={{
                                height: "30%",
                                width: "100%",
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: "column",
                            }}
                        >
                            <div>
                                <button
                                    style={{
                                        borderColor: "#00A3FF",
                                        borderRadius: "30px",
                                        textAlign: "center",
                                        color: "#00A3FF",
                                        backgroundColor: "white",
                                        marginBottom: "10px",
                                        width: "6em",
                                        height: "1.5em",
                                        cursor: "pointer",
                                        marginRight: "10px",
                                    }}
                                    name={initialQuestions[stageNumber - 1]}
                                    onClick={() => {
                                        handleInitialQuestionsChangeYN("Yes");
                                        setStageNumber(stageNumber + 1);
                                    }}
                                >
                                    Yes
                                </button>
                                <button
                                    style={{
                                        borderColor: "#00A3FF",
                                        borderRadius: "30px",
                                        textAlign: "center",
                                        backgroundColor: "white",
                                        color: "#00A3FF",
                                        marginBottom: "10px",
                                        width: "6em",
                                        height: "1.5em",
                                        cursor: "pointer",
                                    }}
                                    name={initialQuestions[stageNumber - 1]}
                                    onClick={() => {
                                        handleInitialQuestionsChangeYN("No");
                                        setStageNumber(stageNumber + 1);
                                    }}
                                >
                                    No
                                </button>
                            </div>
                            <button
                                style={{
                                    border: "none",
                                    backgroundColor: "transparent",
                                    cursor: "pointer",
                                }}
                                onClick={() => {
                                    setStageNumber(stageNumber + 1);
                                }}
                            >
                                Continue &gt;
                            </button>
                        </div>
                    </div>
                )) ||
                (stageNumber === 5 && (
                    <div
                        style={{
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            flexDirection: "column",
                            width: "60%",
                        }}
                    >
                        <div
                            style={{
                                height: "30%",
                                width: "100%",
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center",
                                flexDirection: "row",
                            }}
                        >
                            <p
                                style={{ cursor: "pointer", fontSize: "20px" }}
                                onClick={() => {
                                    setStageNumber(stageNumber - 1);
                                }}
                            >
                                &lt; Previous
                            </p>
                            <img
                                style={{ width: "40px" }}
                                src="./Logo.svg"
                                alt="Logo"
                            />
                        </div>
                        <div
                            style={{
                                height: "30%",
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: "column",
                            }}
                        >
                            <p>{initialQuestions[stageNumber - 1]}</p>
                        </div>
                        <div
                            style={{
                                height: "30%",
                                width: "100%",
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: "column",
                            }}
                        >
                            <div>
                                <button
                                    style={{
                                        borderColor: "#00A3FF",
                                        borderRadius: "30px",
                                        textAlign: "center",
                                        color: "#00A3FF",
                                        backgroundColor: "white",
                                        marginBottom: "10px",
                                        width: "6em",
                                        height: "1.5em",
                                        cursor: "pointer",
                                        marginRight: "10px",
                                    }}
                                    name={initialQuestions[stageNumber - 1]}
                                    onClick={() => {
                                        handleInitialQuestionsChangeYN("Yes");
                                        setStageNumber(stageNumber + 1);
                                    }}
                                >
                                    Yes
                                </button>
                                <button
                                    style={{
                                        borderColor: "#00A3FF",
                                        borderRadius: "30px",
                                        textAlign: "center",
                                        backgroundColor: "white",
                                        color: "#00A3FF",
                                        marginBottom: "10px",
                                        width: "6em",
                                        height: "1.5em",
                                        cursor: "pointer",
                                    }}
                                    name={initialQuestions[stageNumber - 1]}
                                    onClick={() => {
                                        handleInitialQuestionsChangeYN("No");
                                        setStageNumber(stageNumber + 1);
                                    }}
                                >
                                    No
                                </button>
                            </div>
                        </div>
                    </div>
                )) ||
                (stageNumber === 6 && (
                    <div
                        style={{
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            flexDirection: "column",
                            width: "60%",
                        }}
                    >
                        <div
                            style={{
                                height: "30%",
                                width: "100%",
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center",
                                flexDirection: "row",
                            }}
                        >
                            <p
                                style={{ cursor: "pointer", fontSize: "20px" }}
                                onClick={() => {
                                    setStageNumber(stageNumber - 1);
                                }}
                            >
                                &lt; Previous
                            </p>
                            <img
                                style={{ width: "40px" }}
                                src="./Logo.svg"
                                alt="Logo"
                            />
                        </div>
                        <div
                            style={{
                                height: "30%",
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: "column",
                            }}
                        >
                            <p>{initialQuestions[stageNumber - 1]}</p>
                        </div>
                        <div
                            style={{
                                height: "30%",
                                width: "100%",
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: "column",
                            }}
                        >
                            <div>
                                <button
                                    style={{
                                        borderColor: "#00A3FF",
                                        borderRadius: "30px",
                                        textAlign: "center",
                                        color: "#00A3FF",
                                        backgroundColor: "white",
                                        marginBottom: "10px",
                                        width: "6em",
                                        height: "1.5em",
                                        cursor: "pointer",
                                        marginRight: "10px",
                                    }}
                                    name={initialQuestions[stageNumber - 1]}
                                    onClick={() => {
                                        handleInitialQuestionsChangeYN("Yes");
                                        setStageNumber(stageNumber + 1);
                                    }}
                                >
                                    Yes
                                </button>
                                <button
                                    style={{
                                        borderColor: "#00A3FF",
                                        borderRadius: "30px",
                                        textAlign: "center",
                                        backgroundColor: "white",
                                        color: "#00A3FF",
                                        marginBottom: "10px",
                                        width: "6em",
                                        height: "1.5em",
                                        cursor: "pointer",
                                    }}
                                    name={initialQuestions[stageNumber - 1]}
                                    onClick={() => {
                                        handleInitialQuestionsChangeYN("No");
                                        setStageNumber(stageNumber + 1);
                                    }}
                                >
                                    No
                                </button>
                            </div>
                        </div>
                    </div>
                )) ||
                (stageNumber === 7 && (
                    <div
                        style={{
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            flexDirection: "column",
                            width: "60%",
                        }}
                    >
                        <div
                            style={{
                                height: "30%",
                                width: "100%",
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center",
                                flexDirection: "row",
                            }}
                        >
                            <p
                                style={{ cursor: "pointer", fontSize: "20px" }}
                                onClick={() => {
                                    setStageNumber(stageNumber - 1);
                                }}
                            >
                                &lt; Previous
                            </p>
                            <img
                                style={{ width: "40px" }}
                                src="./Logo.svg"
                                alt="Logo"
                            />
                        </div>
                        <div
                            style={{
                                height: "30%",
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: "column",
                            }}
                        >
                            <p>{initialQuestions[stageNumber - 1]}</p>
                            <p style={{ fontSize: "12px", fontWeight: "100" }}>
                                *Disclaimer* After answering this question, you
                                will begin a 5 minute verbal conversation with
                                Ava. This will save you the wait at the doctor’s
                                office.
                            </p>
                        </div>
                        <div
                            style={{
                                height: "30%",
                                width: "100%",
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: "column",
                            }}
                        >
                            <input
                                style={{
                                    borderColor: "#00A3FF",
                                    borderRadius: "30px",
                                    textAlign: "center",
                                    color: "#00A3FF",
                                    marginBottom: "10px",
                                    width: "30em",
                                    height: "1.5em",
                                }}
                                type="text"
                                placeholder="e.g. I have a really bad sore throat"
                                name={initialQuestions[stageNumber - 1]}
                                onChange={handleInitialQuestionsChange}
                            />
                            <button
                                style={{
                                    border: "none",
                                    backgroundColor: "transparent",
                                    cursor: "pointer",
                                }}
                                onClick={startConversation}
                            >
                                Start Conversation &gt;
                            </button>
                        </div>
                    </div>
                ))
            ) : (
                <div
                    style={{
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                        height: "100%",
                    }}
                >
                    <div style={{ width: "70%", height: "100%" }}>
                        <div
                            style={{
                                display: "flex",
                                height: "20%",
                                alignItems: "center",
                                justifyContent: "center",
                                flexDirection: "column",
                                color: "white",
                            }}
                        >
                            <div
                                style={{
                                    display: "flex",
                                    width: "100%",
                                    alignItems: "center",
                                    justifyContent: "space-between",
                                }}
                            >
                                <p style={{ fontSize: "24px" }}>
                                    Meet your nurse:
                                </p>
                                <img
                                    style={{ width: "40px" }}
                                    src="./Logo.svg"
                                    alt="Logo"
                                />
                            </div>
                            <div
                                style={{
                                    display: "flex",
                                    width: "100%",
                                    alignItems: "start",
                                    fontSize: "20px",
                                }}
                            >
                                Ava
                            </div>
                        </div>
                        <div className="chat-history">
                            {chatHistory.map((msg, index) => (
                                <div
                                    style={{
                                        marginBottom: "20px",
                                    }}
                                    key={index}
                                    className={msg.role}
                                >
                                    <strong>
                                        {msg.role === "user"
                                            ? "You"
                                            : "Virtual Nurse"}
                                        :
                                    </strong>{" "}
                                    {msg.content}
                                </div>
                            ))}
                        </div>
                        {!isConversationFinished && (
                            <div
                                style={{
                                    display: "flex",
                                    height: "20%",
                                    justifyContent: "center",
                                    alignItems: "center",
                                }}
                            >
                                <input
                                    style={{
                                        borderColor: "#00A3FF",
                                        borderRadius: "30px",
                                        textAlign: "center",
                                        color: "#00A3FF",
                                        marginBottom: "10px",
                                        width: "30em",
                                        height: "1.5em",
                                        marginRight: "10px",
                                    }}
                                    type="text"
                                    value={userMessage}
                                    onChange={(e) =>
                                        setUserMessage(e.target.value)
                                    }
                                    onKeyDown={(event) => {
                                        if (event.key === "Enter") {
                                            sendMessage();
                                        }
                                    }}
                                    placeholder="Type your message..."
                                />
                                <button
                                    style={{
                                        borderColor: "#00A3FF",
                                        borderRadius: "30px",
                                        textAlign: "center",
                                        backgroundColor: "white",
                                        color: "#00A3FF",
                                        marginBottom: "10px",
                                        width: "6em",
                                        height: "1.5em",
                                        cursor: "pointer",
                                    }}
                                    onClick={sendMessage}
                                >
                                    Send
                                </button>
                            </div>
                        )}
                        {isConversationFinished && (
                            <div
                                style={{
                                    display: "flex",
                                    height: "20%",
                                    justifyContent: "center",
                                    alignItems: "center",
                                }}
                            >
                                <h2>Conversation Finished</h2>
                                <button onClick={fetchReport}>
                                    Get Report
                                </button>
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;
