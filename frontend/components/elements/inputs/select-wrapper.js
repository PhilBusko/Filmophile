/**************************************************************************************************
SELECT WRAPPER ELEMENT
**************************************************************************************************/
import * as React from 'react';
import PropTypes from 'prop-types';
import './inputs.scss'

class SelectWrapper extends React.Component {

    static propTypes = {
        options: PropTypes.array.isRequired,  
        label: PropTypes.string.isRequired,  
        updateSelection: PropTypes.func.isRequired,
    }

    state = {
        value: 0,
    }

    updateValue = (synthEvt) => {
        // not sure if the state should be maintained within the control
        // but don't want to send synthetic event to parent
        // value is a string by default

        let newValue = synthEvt.target.value;
        this.setState({value: newValue});
        this.props.updateSelection(newValue);
    }

    render() {
        let ctrlId = this.props.label.toLowerCase().replace(' ', '') + '_slct'
        return (
            <div className='input-wrapper'>
                <label htmlFor={ ctrlId }>{ this.props.label }: </label>
                <select id={ ctrlId } onChange={ this.updateValue } value={ this.state.value }>
                    {this.props.options.map((opt, idx) => (
                        <option key={ idx } value={ opt['key'] }>{ opt['value'] }</option>
                    ))}
                </select>
            </div>
        );
    }
}

export default SelectWrapper;
