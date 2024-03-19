import React, { useState, useEffect } from 'react'
import cn from 'classnames'
import styles from './style.module.css'

const SelectGroup ({
    options
}) => {
    const [ selectedOption, setSelectedOption ] = useState(value)

  handleOptionSelect = (option) => {
    this.setState(() => ({ selectedOption: option }));
  };

  render() {
    return (
      <>
        <Select
          options={options}
          value={this.state.selectedOption}
          onChange={this.handleOptionSelect}
        />
        Selected Option: "{this.state.selectedOption}"
      </>
    );
  }
};

export default SelectGroup;