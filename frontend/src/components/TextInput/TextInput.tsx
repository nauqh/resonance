import { ChangeEvent } from "react";
import "./TextInput.css";

interface TextInputProps {
	label: string;
	placeholder: string;
	value: string;
	onChange: (text: string) => void;
}

const TextInput = ({ label, placeholder, value, onChange }: TextInputProps) => {
	const handleChange = (e: ChangeEvent<HTMLTextAreaElement>) => {
		onChange(e.target.value);
	};

	return (
		<div className="contact__form-div contact__form-area">
			<label className="contact__form-tag">{label}</label>
			<textarea
				placeholder={placeholder}
				className="contact__form-input"
				value={value}
				onChange={handleChange}
			/>
		</div>
	);
};

export default TextInput;
