/**************************************************************************************************
TEXT WRAPPER ELEMENT
**************************************************************************************************/
import * as React from 'react';
import PropTypes from 'prop-types';
import './inputs.scss'

class TextWrapper extends React.Component {

    static propTypes = {
        label: PropTypes.string.isRequired,  
        updateText: PropTypes.func.isRequired,
    }

    state = {
        value: '',
    }

    updateValue = (synthEvt) => {
        let newValue = synthEvt.target.value;
        this.setState({ value: newValue });
        this.props.updateText(newValue);
    }

    render() {
        let ctrlId = this.props.label.toLowerCase().replace(' ', '') + '_nptx'
        return (
            <div className='input-wrapper'>
                <label htmlFor={ ctrlId }>{ this.props.label }: </label>
                <input type={ 'text' } value={ this.state.value } onChange={ this.updateValue } 
                    className='input-format' maxLength={ 10 }></input>
            </div>
        );
    }
}

export default TextWrapper;
