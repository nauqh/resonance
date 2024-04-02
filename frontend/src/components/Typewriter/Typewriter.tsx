import React, { useState, useEffect } from "react";
import "./Typewriter.css";

interface TypewriterProps {
	text: string;
	delay: number;
	onComplete?: () => void;
}

const Typewriter: React.FC<TypewriterProps> = ({ text, delay, onComplete }) => {
	const [currentText, setCurrentText] = useState<string>("");
	const [currentIndex, setCurrentIndex] = useState<number>(0);

	useEffect(() => {
		const typeNextCharacter = () => {
			if (currentIndex < text.length) {
				setCurrentText((prevText) => prevText + text[currentIndex]);
				setCurrentIndex((prevIndex) => prevIndex + 1);
			} else {
				if (onComplete) {
					onComplete();
				}
			}
		};

		const timeout = setTimeout(typeNextCharacter, delay);

		return () => clearTimeout(timeout);
	}, [currentIndex, delay, onComplete, text]);

	return (
		<>
			<span className="typewriter__content">{currentText}</span>
		</>
	);
};

export default Typewriter;
