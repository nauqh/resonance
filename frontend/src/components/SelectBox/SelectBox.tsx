import React, { useState, ChangeEvent } from "react";
import "./SelectBox.css";

interface SelectBoxProps {
	labell: string;
	labelr: string;
	options: string[];
	onChange: (selectedOption: string) => void;
}

const SelectBox: React.FC<SelectBoxProps> = ({
	labell,
	labelr,
	options,
	onChange,
}) => {
	const [selectedOption, setSelectedOption] = useState<string>("");
	const [startYear, setStartYear] = useState<string>("");
	const [endYear, setEndYear] = useState<string>("");
	const [error, setError] = useState<string>("");

	const handleOptionChange = (e: ChangeEvent<HTMLSelectElement>) => {
		const value = e.target.value;
		setSelectedOption(value);
		onChange(value);
	};

	const handleStartYearChange = (e: ChangeEvent<HTMLInputElement>) => {
		const value = e.target.value;
		setStartYear(value);
		validateYearRange(value, endYear);
	};

	const handleEndYearChange = (e: ChangeEvent<HTMLInputElement>) => {
		const value = e.target.value;
		setEndYear(value);
		validateYearRange(startYear, value);
	};

	const validateYearRange = (start: string, end: string) => {
		if (parseInt(start) > parseInt(end)) {
			setError("Year range is invalid");
		} else {
			setError("");
		}
	};

	return (
		<>
			<div className="select__box">
				<div className="select__box-item">
					<label className="select__box-label">{labell}</label>
					<select
						className="select__box-select"
						value={selectedOption}
						onChange={handleOptionChange}
					>
						{options.map((option, index) => (
							<option key={index} value={option}>
								{option}
							</option>
						))}
					</select>
				</div>

				<div className="select__box-item">
					<label className="select__box-label">{labelr}</label>
					<div className="year-box">
						<input
							className="select__box-text"
							type="text"
							placeholder="Start"
							value={startYear}
							onChange={handleStartYearChange}
						/>
						<span style={{ paddingTop: "0.5rem" }}>-</span>
						<input
							className="select__box-text"
							type="text"
							placeholder="End"
							value={endYear}
							onChange={handleEndYearChange}
						/>
					</div>
					{error && <div className="select__box-error">{error}</div>}
				</div>
			</div>
		</>
	);
};

export default SelectBox;
