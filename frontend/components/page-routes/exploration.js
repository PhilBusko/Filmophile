/**************************************************************************************************
EXPLORATION PAGE
**************************************************************************************************/
import * as React from 'react';
import axios from 'axios';
import { When } from 'react-if';
import Plot from 'react-plotly.js';
import MenuLayout from '../layouts/menu-layout'

class Exploration extends React.Component {

    loadingIcon = require('../assets/controls/loading_cat.gif')

    state = {
        totalsPlot: null,
        scoresPlot: null,
    }

    componentDidMount() {
        axios({
            url: 'api/movies/totals_plot/',
            method: 'get',
        }).then( success => {
            var jsonPlot = JSON.parse(success.data);
            this.setState({totalsPlot: jsonPlot});
        }).catch( error => {
            console.log(error);
        });

        axios({
            url: 'api/movies/scores_plot/',
            method: 'get',
        }).then( success => {
            var jsonPlot = JSON.parse(success.data);
            this.setState({scoresPlot: jsonPlot});
        }).catch( error => {
            console.log(error);
        });
    }

    render() {
        let totalsPlot = this.state.totalsPlot;
        let scoresPlot = this.state.scoresPlot;

        return (
            <MenuLayout>
                <div className='pure-g spacing-outer'>

                    <div className='pure-u-1'>
                        <div className='spacing-inner page-title'>
                            Exploration
                        </div>
                    </div>

                    <div className='pure-u-1'>
                        <div className='spacing-inner heading'>
                            Streaming Service Info
                        </div>
                    </div>

                    <div className='pure-u-1 pure-u-xxxl-1-2'>
                        <div className='spacing-inner center-both'>
                            <When condition={ !!totalsPlot }>
                                { () =>
                                    <Plot 
                                        data={ totalsPlot.data }
                                        layout={ totalsPlot.layout }
                                    />
                                }
                            </When>
                            <When condition={ !totalsPlot }>
                                <div style={{ width: '700px', height: '500px', border: '1px solid MediumSlateBlue'}} className='center-both'>
                                    <img src={ this.loadingIcon } className='loading-icon' alt='loading'/>
                                </div>
                            </When>
                        </div>
                    </div>

                    <div className='pure-u-1 pure-u-xxxl-1-2'>
                        <div className='spacing-inner center-both'>
                            <When condition={ !!scoresPlot }>
                                { () =>
                                    <Plot 
                                        data={ scoresPlot.data }
                                        layout={ scoresPlot.layout }
                                    />
                                }
                            </When>
                            <When condition={ !scoresPlot }>
                                <div style={{ width: '700px', height: '500px', border: '1px solid MediumSlateBlue'}} className='center-both'>
                                    <img src={ this.loadingIcon } className='loading-icon' alt='loading'/>
                                </div>
                            </When>
                        </div>
                    </div>

                </div>
            </MenuLayout>
        );
    }
}

export default Exploration;
