/**************************************************************************************************
PLOT WRAPPER ELEMENT
**************************************************************************************************/
import * as React from 'react';
import PropTypes from 'prop-types';
import { When } from 'react-if';
import Plot from 'react-plotly.js'
import LoadingIcon from './loading-icon'
import './plot-wrapper.scss'

class PlotWrapper extends React.Component {

    static propTypes = {
        plotConfig: PropTypes.object.isRequired,
        sizeClass: PropTypes.string.isRequired, 
        isStatic: PropTypes.bool.isRequired,  
    }

    static defaultProps = {
        isStatic: false,
    }

    state = {}

    render() {
        return (
            <div className='plot-wrapper'>
                <When condition={ Object.keys(this.props.plotConfig).length > 0 }>
                    { () =>
                        <Plot 
                            data={ this.props.plotConfig.data }
                            layout={ this.props.plotConfig.layout }
                            config={{ 'staticPlot': this.props.isStatic }}
                        />
                    }
                </When>
                <When condition={ Object.keys(this.props.plotConfig).length == 0 }>
                    <div className={ this.props.sizeClass }>
                        <LoadingIcon/>
                    </div>
                </When>
            </div>
        );
    }
}

export default PlotWrapper;

