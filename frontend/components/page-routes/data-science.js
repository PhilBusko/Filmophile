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
    dataClean = require('../assets/backgrounds/data-clean.png')
    multihotDiagram = require('../assets/backgrounds/multihot.png')

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

                    <div className='pure-u-1 pure-u-xl-3-24'> </div>
                    <div className='pure-u-1 pure-u-xl-18-24'>
                        <div className='spacing-inner' style={{ marginBottom: '20px' }}>
                            This website provides movie recommendations for streaming services. 
                            For that, it needs movie data, user scores, and a customized algorithm. 
                            The algorithm will take the user's scores and create a model based on the movie information. 
                            So for example, if the user tends to give high scores to Fantasy movies,
                            but low scores to Horror movies, 
                            then the algorithm's recommendations will reflect that. 
                            Altogether, this site showcases three aspects of data science: 
                            data extraction and cleaning, database storage and retrieval, and a classification algorithm. 
                            This page provides greater detail for how the recommendation model is trained.
                       </div>
                    </div>
 
                    <div className='pure-u-1'>
                        <div className='spacing-inner subheading'>
                            1] Data Extraction & Cleaning
                        </div>
                    </div>
                    <div className='pure-u-1 pure-u-xl-1-2'>
                        <div className='spacing-inner'>
                            <div>
                                There are 3 data sources used in this project. 
                                The Movie Database (TMDB) is the primary data source, and it's movie-id is used as the unique movie id.
                                The Reelgood site provides the information about which movies and shows are currently available on streaming services.
                                The Internet Movie Database (IMDB) provides complimentary movie data, such as IMDB Score. 
                                The TMDB data is obtained through their very nice web-API.
                                The Reelgood and IMDB data are obtained by scraping.
                            </div>
                            <br></br>
                            <div>
                                The adjacent table shows all of the features used in the recommendation algorithm. 
                                It also shows for each source how much of each feature is available.
                                The Union-All column shows the availability of final data for the project. 
                                Typically the final value used from the disparate sources is just the highest value. 
                                For example, if TMDB gives a runtime of 87 mins, and IMDB gives 82 mins, 
                                then 87 mins is taken as the final value. 
                                However, a column marked with a * denotes that the final value relies on weighted values from all the data sources. 
                                A value has to occur at least twice in common to qualify as a final data value.
                                The following diagram shows an example of this. 
                            </div>
                            <br></br>
                            <div className='center-both'>
                                <img src={ this.dataClean } style={{ height: '130px', marginTop: '10px'}}
                                    alt='Example cleaning of categorical list data.'></img>
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

                    <div className='pure-u-1'>
                        <div className='spacing-inner subheading'>
                            2] Feature Engineering
                        </div>
                    </div>
                    <div className='pure-u-1 pure-u-xl-1-2'>
                        <div className='spacing-inner'>
                            <div>
                                <span className='entry-title'>Numeric: </span>
                                The numeric features are year, run time, budget, gross, imdb-score, imdb-votes. 
                                These features require no engineering, and will only be standardized later.
                            </div>
                            <br></br>
                            <div>
                                <span className='entry-title'>Categorical: </span>
                                The categorical features are rating, companies, country, language, crew, cast. 
                                Most of these features can be one-hot encoded with no problems.
                                These features have a scalar value, 
                                and their unique values are numbered in the low hundreds.  
                                Meaning, that when one-hot encoded, they won't create an untenable number of columns.
                                <br></br>
                                &nbsp;&nbsp;&nbsp;&nbsp;However, the columns Crew and Cast are different. 
                                These features have list values, so they include the credits for director, producer, etc. 
                                Each list can have up to 3 entries.
                                These features are first filtered and before they are one-hot encoded, 
                                their unique values only number in the hundreds.
                            </div>
                            <br></br>
                        </div>
                    </div>
                    <div className='pure-u-1 pure-u-xl-1-2'>
                        <div className='spacing-inner'>
                            <span className='entry-title'>Categorical for MultiHot Encoding: </span>
                            The feature for multihot encoding is Genres.
                            Multihot encoding refers to the onehot encoding of a list variable. 
                            The hot-columns have a 1 if their row includes the value that the column corresponds to,
                            and a 0 otherwise.
                            Though a pandas dataframe has a standard&nbsp;
                            <a href='https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.get_dummies.html' 
                                className='link-format' target='blank_'>onehot encoder</a>,
                            there is no implementation for a multihot encoder. 
                            I ultimately used&nbsp;
                            <a href='https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MultiLabelBinarizer.html' 
                                className='link-format' target='blank_'>MultiLabelBinarizer</a>
                            &nbsp;to implement the solution.
                            The following diagram shows an example multihot encode.
                        </div>
                    </div>
                    <div className='pure-u-1'>
                        <div className='spacing-inner center-both'>
                            <img src={ this.multihotDiagram } alt='Multihot Encoding' 
                                style={{ height: '210px' }}></img>
                        </div>
                    </div>

                    <div className='pure-u-1'>
                        <div className='spacing-inner subheading'>
                            3] Target Variable - User Scores
                        </div>
                    </div>
                    <div className='pure-u-1 pure-u-lg-1-2'>
                        <div className='spacing-inner'>
                            <div>
                                The user-score is a value from 1 to 3 that the site's user assigns to any movies they've seen.
                                It's an indication of how much they liked the movie:
                                1 means they hate it, 2 means it's ok, and 3 means they loved it. 
                                Because the user has three different scores available, 
                                the movie recommendations also come in three types: Love It, Maybe, and Don't Bother.
                                <br></br>
                                &nbsp;&nbsp;&nbsp;&nbsp;The user score is the algorithm's target variable. 
                                That is, the algorithm uses the movies' features to find a pattern 
                                that will match how the user scored the movies. 
                                Each user will score movies differently, 
                                so each user has a specific model trained for them. 
                                The adjacent plot shows a sample distribution of a user's scores for movies.
                                Notice that the target variable has a considerable imbalance.
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
                                <div style={{ width: '400px', height: '300px', border: '1px solid MediumSlateBlue'}} className='center-both'>
                                    <img src={ this.loadingIcon } className='loading-icon' alt='loading'/>
                                </div>
                            </When>
                        </div>
                    </div>

                    <div className='pure-u-1'>
                        <div className='spacing-inner subheading'>
                            4] Choosing a Classification Algorithm
                        </div>
                    </div>
                    <div className='pure-u-1 pure-u-xl-20-24'>
                        <div className='spacing-inner'>
                            <div>
                                In general there are many suitable supervised learning classification algorithms available.
                                The typical process is to start with a baseline algorithm, like logistic regression, 
                                and then move to more complex options in search of higher accuracy or other metrics. 
                                However, this project was met with an additional restriction: 
                                several algorithms' predictions are not usable because they are extremely imbalanced.
                                Therefore the first question to answer becomes which algorithm to use. 
                            </div>
                            <br></br>
                            <div>
                                In the search for general algorithm predictions, 6 well-known classifiers were used. 
                                The classifiers were run with their base configuration from scikit-learn; 
                                meaning there is no tuning, grid search, etc.
                                As shown on the adjacent graph, most algorithms do not perform well with this dataset, 
                                with 4 of 6 being completely unusable.
                                Therefore, SVM is the only viable option to proceed with. 
                            </div>
                        </div>
                    </div>
                    <div className='pure-u-1'>
                        <div className='spacing-inner center-both'>
                            <When condition={ !!this.state.restrictedClassifiers }>
                            { () =>
                                <Plot data={ this.state.restrictedClassifiers.data }
                                    layout={ this.state.restrictedClassifiers.layout }
                                />
                            }
                            </When>
                            <When condition={ !this.state.restrictedClassifiers }>
                                <div style={{ width: '800px', height: '500px', border: '1px solid MediumSlateBlue'}} className='center-both'>
                                    <img src={ this.loadingIcon } className='loading-icon' alt='loading'/>
                                </div>
                            </When>
                        </div>
                    </div>



                    <div className='pure-u-1'>
                        <div className='spacing-inner subheading'>
                            5] Tuning Support Vector Machine
                        </div>
                    </div>
                    <div className='pure-u-20-24'>
                        <div className='spacing-inner'>
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
