/**************************************************************************************************
BUTTON WRAPPER ELEMENT
**************************************************************************************************/
import * as React from 'react';
import PropTypes from 'prop-types';
import './inputs.scss'

class ButtonWrapper extends React.Component {

    static propTypes = {
        label: PropTypes.string.isRequired,  
        updateClick: PropTypes.func.isRequired,
    }

    state = {
    }

    handleClick = (synthEvt) => {
        this.props.updateClick();
    }

    render() {
        let ctrlId = this.props.label.toLowerCase().replace(' ', '') + '_btn'
        return (
            <div className='input-wrapper'>
                <button id={ ctrlId } onClick={ this.handleClick } className='button-format'>{ this.props.label }</button>
            </div>
        );
    }
}

export default ButtonWrapper;

