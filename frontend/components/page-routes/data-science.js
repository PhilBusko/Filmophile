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

    loadingIcon = require('../assets/controls/loading_cat.gif')

    state = {
        dataHistory: null,
        votePlot: null,
        restrictedClassifiers: null,
    }

    componentDidMount() {
        axios({
            url: 'api/movies/data_history/',
            method: 'get',
        }).then( success => {
            //console.log(success.data);
            this.setState({dataHistory: success.data});
        }).catch( error => {
            console.log(error);
        });

        axios({
            url: 'api/movies/vote_plot/',
            method: 'get',
        }).then( success => {
            var jsonPlot = JSON.parse(success.data);
            this.setState({votePlot: jsonPlot});
        }).catch( error => {
            console.log(error);
        });

        axios({
            url: 'api/movies/restricted_classifiers/',
            method: 'get',
        }).then( success => {
            var jsonPlot = JSON.parse(success.data);
            this.setState({restrictedClassifiers: jsonPlot});
        }).catch( error => {
            console.log(error);
        });
    }

    render() {
        return (
            <MenuLayout>
                <div className='pure-g spacing-outer'>

                    <div className='pure-u-1'>
                        <div className='spacing-inner page-title'>
                            Data Science
                        </div>
                    </div>

                    <div className='pure-u-1'>
                        <div className='spacing-inner'>
                            <span className='entry-title'>Non-Technical Presentation: </span>
                            <a href='https://docs.google.com/presentation/d/1aqI7jCI6Vg6Tp6t-_Gk7SuNp51bvD_885ZGPFv6b-ZY/edit?usp=sharing'
                                className='link-format' target='blank_'>Google Slides</a>
                        </div>
                    </div>

                    <div className='pure-u-1 pure-u-xl-1-2'>
                        <div className='spacing-inner'>
                            <div className='entry-title' style={{ textDecoration: 'underline' }}>1] Data Scraping & Cleaning</div>
                            <br></br>
                            <div>
                                There are 3 sources of data used in this project. 
                                The Movie Database (TMDB) is the primary data source, and it's movie-id is the project's movie-id.
                                The Reelgood site provides the information about which movies and shows are currently available on streaming services.
                                The Internet Movie Database (IMDB) provides complimentary movie data, such as IMDB Score. 
                                The TMDB data is obtained through their very nice web-API.
                                The Reelgood and IMDB data are obtained by scraping the sites.
                            </div>
                            <br></br>
                            <div>
                                The adjacent table shows all of the features used in the recommendation algorithm. 
                                It also shows a breakdown for each source of how much of each feature is available.
                                The Union-All column shows the occurence of final data as used in the project. 
                                A column marked with a * denotes that the final data relies on majority values from the data sources. 
                                So even if one data source has values for a particular movie, 
                                those values may not show up in the final feature if they are not corroborated by the other sources.
                            </div>
                        </div>
                    </div>
                    <div className='pure-u-1 pure-u-xl-1-2'>
                        <div className='spacing-inner small-font'>
                            <When condition={ !!this.state.dataHistory }>
                            { () =>
                                <TableWrapper tableRows={ this.state.dataHistory }></TableWrapper>
                            }
                            </When>
                            <When condition={ !this.state.dataHistory }>
                                <div style={{ width: '510px', height: '460px', border: '1px solid MediumSlateBlue'}} className='center-both'>
                                    <img src={ this.loadingIcon } className='loading-icon' alt='loading'/>
                                </div>
                            </When>
                        </div>
                    </div>

                    <div className='pure-u-1 pure-u-lg-1-2'>
                        <div className='spacing-inner'>
                            <div className='entry-title' style={{ textDecoration: 'underline' }}>2] Target Variable: User Votes</div>
                            <br></br>
                            <div>
                                The recommendation system works based on votes that the user casts for movies and TV shows.
                                Vote 1 means they hate it, 2 means it's ok, and 3 means they love it. 
                                The classification algorithm uses these votes as the target variable when training the model. 
                                The predictions made by the algorithm are then used as the recommendation level, 
                                for example, a predicted class of 3 means that the user will probably really like the movie.
                                One advantage of this system over the conventional mass-marketing&nbsp;
                                <a className='link-format' href='https://en.wikipedia.org/wiki/Recommender_system'>recommender system</a> is
                                that it's personalized to the user.
                                A disadvantage of this system is that it requires hundreds of votes to produce useful results.
                            </div>
                            <br></br>
                            <div>
                                The adjacent plot shows a sample distribution of user votes for movies.
                                The takeaway here is that the training target variable has a considerable imbalance.
                            </div>
                        </div>
                    </div>
                    <div className='pure-u-1 pure-u-lg-1-2'>
                        <div className='spacing-inner'>
                            <When condition={ !!this.state.votePlot }>
                            { () =>
                                <Plot data={ this.state.votePlot.data }
                                    layout={ this.state.votePlot.layout }
                                    config={{ 'staticPlot': true }} />
                            }
                            </When>
                            <When condition={ !this.state.votePlot }>
                                <div style={{ width: '400px', height: '400px', border: '1px solid MediumSlateBlue'}} className='center-both'>
                                    <img src={ this.loadingIcon } className='loading-icon' alt='loading'/>
                                </div>
                            </When>
                        </div>
                    </div>

                    <div className='pure-u-20-24'>
                        <div className='spacing-inner'>
                            <div className='entry-title' style={{ textDecoration: 'underline' }}>3] Choosing a Classification Algorithm</div>
                            <br></br>
                            <div>
                                In general there are many suitable supervised learning classification algorithms available.
                                The typical process is to start with a baseline algorithm (like logistic regression), 
                                and then move to more complex options in search of higher accuracy or other metrics. 
                                However, this project was met with an additional restriction: 
                                several algorithms' predictions are totally unacceptable because they are extremely imbalanced.
                            </div>
                            <br></br>
                            <div>
                                The adjacent plot shows this imbalance for 6 popular classifiers. 
                                These classifiers have been run with their base configuration from scikit-learn, 
                                meaning there is no tuning, grid search, etc.
                                By inspecting the plots, it becomes evident that SVM is the only reasonable option to proceed with. 
                            </div>
                        </div>
                    </div>
                    <div className='pure-u-1'>
                        <div className='spacing-inner center-both'>
                            <When condition={ !!this.state.restrictedClassifiers }>
                            { () =>
                                <Plot data={ this.state.restrictedClassifiers.data }
                                    layout={ this.state.restrictedClassifiers.layout }
                                    config={{ 'staticPlot': true }} />
                            }
                            </When>
                            <When condition={ !this.state.restrictedClassifiers }>
                                <div style={{ width: '1000px', height: '700px', border: '1px solid MediumSlateBlue'}} className='center-both'>
                                    <img src={ this.loadingIcon } className='loading-icon' alt='loading'/>
                                </div>
                            </When>
                        </div>
                    </div>

                    <div className='pure-u-20-24'>
                        <div className='spacing-inner'>
                            <div className='entry-title' style={{ textDecoration: 'underline' }}>4] Tuning Support Vector Machine</div>
                            <br></br>
                            <div>
                                Future Work
                            </div>
                            <br></br>
                            <div>
                                . 
                            </div>
                        </div>
                    </div>



                </div>
            </MenuLayout>
        );
    }
}

export default DataScience;
