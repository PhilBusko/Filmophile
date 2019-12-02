/**************************************************************************************************
SELECT WRAPPER ELEMENT
**************************************************************************************************/
import * as React from 'react';
import PropTypes from 'prop-types';
import './select-wrapper.scss'

class SelectWrapper extends React.Component {

    static propTypes = {
        options: PropTypes.array.isRequired,  
        label: PropTypes.string.isRequired,  
        updateSelection: PropTypes.func.isRequired,
    }

    render() {
        let ctrlId = this.props.label.toLowerCase().replace(' ', '') + '_slct'
        return (
            <div className='select-wrapper'>
                <label htmlFor={ ctrlId }>{ this.props.label }: </label>
                <select id={ ctrlId }>
                    {this.props.options.map((opt, idx) => (
                        <option key={ idx } value={ opt }>{ opt }</option>
                    ))}
                </select>
            </div>
        );
    }
}

export default SelectWrapper;
