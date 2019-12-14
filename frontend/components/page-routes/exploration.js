/**************************************************************************************************
EXPLORATION PAGE
**************************************************************************************************/
import * as React from 'react';
import axios from 'axios';
import MenuLayout from '../layouts/menu-layout'
import { PlotWrapper } from '../elements';

class Exploration extends React.Component {

    state = {
        yearsPlot: {},
        countriesPlot: {},
        genresPlot: {},
        genresMoviePlot: {},
        roiPlot: {},
        scoreProfitPlot: {},
        totalsPlot: {},
        scoresPlot: {},
    }

    componentDidMount() {
        let DELAY = 800;

        setTimeout( () => {
            axios({
                url: 'api/movies/years_plot/',
            }).then( success => {
                //console.log(success.data);
                this.setState({ yearsPlot: JSON.parse(success.data) });
            }).catch( error => {
                console.log(error);
            });
        }, 0);

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
        }, DELAY * 5);

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
        }, DELAY * 2);

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
                            <PlotWrapper plotConfig={ this.state.yearsPlot } sizeClass='medium-plot'/>
                        </div>
                        <div className='spacing-inner-large center-both'>
                            <PlotWrapper plotConfig={ this.state.countriesPlot } sizeClass='medium-plot'/>
                        </div>

                        <div className='spacing-inner-large center-both'>
                            <PlotWrapper plotConfig={ this.state.genresPlot } sizeClass='large-plot' isStatic={ true } />
                        </div>
                        <div className='spacing-inner-large center-both'>
                            <PlotWrapper plotConfig={ this.state.genresMoviePlot } sizeClass='small-plot' isStatic={ true } />
                        </div>

                        <div className='spacing-inner-large center-both'>
                            <PlotWrapper plotConfig={ this.state.roiPlot } sizeClass='large-plot'/>
                        </div>
                        <div className='spacing-inner-large center-both'>
                            <PlotWrapper plotConfig={ this.state.scoreProfitPlot } sizeClass='small-plot'/>
                        </div>
                    </div>

                    <div className='pure-u-1'>
                        <div className='spacing-inner heading'>
                            Streaming Service Graphs
                        </div>
                    </div>
                    <div className='pure-u-1 even-panel spacing-outer'>

                        <div className='spacing-inner-large center-both'>
                            <PlotWrapper plotConfig={ this.state.totalsPlot } sizeClass='medium-plot'/>
                        </div>
                        <div className='spacing-inner-large center-both'>
                            <PlotWrapper plotConfig={ this.state.scoresPlot } sizeClass='medium-plot'/>
                        </div>

                    </div>
                </div>
            </MenuLayout>
        );
    }
}

export default Exploration;
