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
        yearsPlot: null,
        countriesPlot: null,
        genresPlot: null,
        genresMoviePlot: null,
        roiPlot: null,
        scoreProfitPlot: null,
        totalsPlot: null,
        scoresPlot: null,
    }

    componentDidMount() {
        let DELAY = 800;

        axios({
            url: 'api/movies/years_plot/',
        }).then( success => {
            this.setState({ yearsPlot: JSON.parse(success.data) });
        }).catch( error => {
            console.log(error);
        });

        setTimeout( () => {
            axios({
                url: 'api/movies/countries_plot/',
            }).then( success => {
                this.setState({ countriesPlot: JSON.parse(success.data) });
            }).catch( error => {
                console.log(error);
            });
        }, DELAY * 1);

        setTimeout( () => {
            axios({
                url: 'api/movies/genres_plot/',
            }).then( success => {
                this.setState({ genresPlot: JSON.parse(success.data) });
            }).catch( error => {
                console.log(error);
            });
        }, DELAY * 2);

        setTimeout( () => {
            axios({
                url: 'api/movies/genresmovie_plot/',
            }).then( success => {
                this.setState({ genresMoviePlot: JSON.parse(success.data) });
            }).catch( error => {
                console.log(error);
            });
        }, DELAY * 3);

        setTimeout( () => {
            axios({
                url: 'api/movies/roi_plot/',
            }).then( success => {
                this.setState({ roiPlot: JSON.parse(success.data) });
            }).catch( error => {
                console.log(error);
            });
        }, DELAY * 4);

        setTimeout( () => {
            axios({
                url: 'api/movies/scoreprofit_plot/',
            }).then( success => {
                this.setState({ scoreProfitPlot: JSON.parse(success.data) });
            }).catch( error => {
                console.log(error);
            });
        }, DELAY * 5);

        setTimeout( () => {
            axios({
                url: 'api/movies/totals_plot/',
            }).then( success => {
                this.setState({ totalsPlot: JSON.parse(success.data) });
            }).catch( error => {
                console.log(error);
            });
        }, DELAY * 6);

        setTimeout( () => {
            axios({
                url: 'api/movies/scores_plot/',
            }).then( success => {
                this.setState({ scoresPlot: JSON.parse(success.data) });
            }).catch( error => {
                console.log(error);
            });
        }, DELAY * 7);
    }

    render() {
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
                            Movie Industry Graphs
                        </div>
                    </div>
                    <div className='pure-u-1 even-panel spacing-outer'>

                        <div className='spacing-inner-large center-both'>
                            <When condition={ !!this.state.yearsPlot }>
                                { () =>
                                    <Plot 
                                        data={ this.state.yearsPlot.data }
                                        layout={ this.state.yearsPlot.layout }
                                    />
                                }
                            </When>
                            <When condition={ !this.state.yearsPlot }>
                                <div style={{ width: '600px', height: '400px', border: '1px solid MediumSlateBlue'}} className='center-both'>
                                    <img src={ this.loadingIcon } className='loading-icon' alt='loading'/>
                                </div>
                            </When>
                        </div>

                        <div className='spacing-inner-large center-both'>
                            <When condition={ !!this.state.countriesPlot }>
                                { () =>
                                    <Plot 
                                        data={ this.state.countriesPlot.data }
                                        layout={ this.state.countriesPlot.layout }
                                    />
                                }
                            </When>
                            <When condition={ !this.state.countriesPlot }>
                                <div style={{ width: '600px', height: '400px', border: '1px solid MediumSlateBlue'}} className='center-both'>
                                    <img src={ this.loadingIcon } className='loading-icon' alt='loading'/>
                                </div>
                            </When>
                        </div>

                        <div className='spacing-inner-large center-both'>
                            <When condition={ !!this.state.genresPlot }>
                                { () =>
                                    <Plot 
                                        data={ this.state.genresPlot.data }
                                        layout={ this.state.genresPlot.layout }
                                    />
                                }
                            </When>
                            <When condition={ !this.state.genresPlot }>
                                <div style={{ width: '700px', height: '400px', border: '1px solid MediumSlateBlue'}} className='center-both'>
                                    <img src={ this.loadingIcon } className='loading-icon' alt='loading'/>
                                </div>
                            </When>
                        </div>

                        <div className='spacing-inner-large center-both'>
                            <When condition={ !!this.state.genresMoviePlot }>
                                { () =>
                                    <Plot 
                                        data={ this.state.genresMoviePlot.data }
                                        layout={ this.state.genresMoviePlot.layout }
                                    />
                                }
                            </When>
                            <When condition={ !this.state.genresMoviePlot }>
                                <div style={{ width: '500px', height: '400px', border: '1px solid MediumSlateBlue'}} className='center-both'>
                                    <img src={ this.loadingIcon } className='loading-icon' alt='loading'/>
                                </div>
                            </When>
                        </div>

                        <div className='spacing-inner-large center-both'>
                            <When condition={ !!this.state.roiPlot }>
                                { () =>
                                    <Plot 
                                        data={ this.state.roiPlot.data }
                                        layout={ this.state.roiPlot.layout }
                                    />
                                }
                            </When>
                            <When condition={ !this.state.roiPlot }>
                                <div style={{ width: '700px', height: '400px', border: '1px solid MediumSlateBlue'}} className='center-both'>
                                    <img src={ this.loadingIcon } className='loading-icon' alt='loading'/>
                                </div>
                            </When>
                        </div>

                        <div className='spacing-inner-large center-both'>
                            <When condition={ !!this.state.scoreProfitPlot }>
                                { () =>
                                    <Plot 
                                        data={ this.state.scoreProfitPlot.data }
                                        layout={ this.state.scoreProfitPlot.layout }
                                    />
                                }
                            </When>
                            <When condition={ !this.state.scoreProfitPlot }>
                                <div style={{ width: '500px', height: '400px', border: '1px solid MediumSlateBlue'}} className='center-both'>
                                    <img src={ this.loadingIcon } className='loading-icon' alt='loading'/>
                                </div>
                            </When>
                        </div>
                    </div>

                    <div className='pure-u-1'>
                        <div className='spacing-inner heading'>
                            Streaming Service Graphs
                        </div>
                    </div>
                    <div className='pure-u-1 even-panel spacing-outer'>

                        <div className='spacing-inner-large center-both'>
                            <When condition={ !!this.state.totalsPlot }>
                                { () =>
                                    <Plot 
                                        data={ this.state.totalsPlot.data }
                                        layout={ this.state.totalsPlot.layout }
                                    />
                                }
                            </When>
                            <When condition={ !this.state.totalsPlot }>
                                <div style={{ width: '600px', height: '400px', border: '1px solid MediumSlateBlue'}} className='center-both'>
                                    <img src={ this.loadingIcon } className='loading-icon' alt='loading'/>
                                </div>
                            </When>
                        </div>

                        <div className='spacing-inner-large center-both'>
                            <When condition={ !!this.state.scoresPlot }>
                                { () =>
                                    <Plot 
                                        data={ this.state.scoresPlot.data }
                                        layout={ this.state.scoresPlot.layout }
                                    />
                                }
                            </When>
                            <When condition={ !this.state.scoresPlot }>
                                <div style={{ width: '600px', height: '400px', border: '1px solid MediumSlateBlue'}} className='center-both'>
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
