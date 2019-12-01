/**************************************************************************************************
RULES-LOADER PAGE
**************************************************************************************************/
import * as React from 'react';
import axios from 'axios';
import { When } from 'react-if';
import Plot from 'react-plotly.js';

import MenuLayout from '../layouts/menu-layout'
import TableWrapper from '../elements/table-wrapper'

class DataScience extends React.Component {

    state = {
        dataHistory: null,
        votePlot: null,
        logregPlot: null,
    }

    componentDidMount() {
        /*
        axios({
            url: 'api/movies/data_history/',
            method: 'get',
            data: { }
        }).then( success => {
            console.log(success.data);

            var updateState = {dataHistory: success.data};
            //this.setState({...this.state, ...updateState});
        }).catch( error => {
            console.log('AXIOS ERROR')
            console.log(error);
        });
        */

        axios({
            url: 'api/movies/vote_plot/',
            method: 'get',
            data: { }
        }).then( success => {
            var jsonPlot = JSON.parse(success.data);
            var updateState = {votePlot: jsonPlot};
            this.setState({...this.state, ...updateState});
        }).catch( error => {
            console.log('Axios Error: api/movies/vote_plot/')
            console.log(error);
        });

        axios({
            url: 'api/movies/analysis_logreg/',
            method: 'get',
            data: { }
        }).then( success => {
            var jsonPlot = JSON.parse(success.data);
            var updateState = {logregPlot: jsonPlot};
            this.setState({...this.state, ...updateState});
        }).catch( error => {
            console.log('Axios Error: api/movies/analysis_logreg/')
            console.log(error);
        });

    }


    render() {
        return (
            <MenuLayout>
                <div className='pure-g'>

                    <div className='pure-u-1 page-title grid-spacing'>
                        Data Science
                    </div>
                    
                    <div className='pure-u-1 grid-spacing'>
                        <span className='entry-title'>Non-Technical Presentation: </span>
                        <a href='https://docs.google.com/presentation/d/1aqI7jCI6Vg6Tp6t-_Gk7SuNp51bvD_885ZGPFv6b-ZY/edit?usp=sharing'
                           className='link-format' target='blank_'>link</a>
                    </div>

                    <div className='pure-u-1 grid-spacing'>
                        <When condition={ !!this.state.dataHistory }>
                        { () =>
                            <TableWrapper tableRows={ this.state.dataHistory }></TableWrapper>
                        }
                        </When>
                        <When condition={ !this.state.dataHistory }>
                        { () =>
                            <div>table loading ...</div>
                        }
                        </When>
                    </div>

                    <div className='pure-u-1 grid-spacing'>
                        <When condition={ !!this.state.votePlot }>
                        { () =>
                            <Plot data={ this.state.votePlot.data }
                                  layout={ this.state.votePlot.layout }
                                  config={{ 'staticPlot': true }} />
                        }
                        </When>
                        <When condition={ !this.state.votePlot }>
                        { () =>
                            <div>plot loading ...</div>
                        }
                        </When>
                    </div>

                    <div className='pure-u-1 grid-spacing'>
                        <When condition={ !!this.state.logregPlot }>
                        { () =>
                            <Plot data={ this.state.logregPlot.data }
                                  layout={ this.state.logregPlot.layout }
                                   />
                        }
                        </When>
                        <When condition={ !this.state.logregPlot }>
                        { () =>
                            <div>plot loading ...</div>
                        }
                        </When>
                    </div>

                </div>
            </MenuLayout>
        );
    }
}

export default DataScience;
