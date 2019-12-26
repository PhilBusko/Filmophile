/**************************************************************************************************
DATA SCIENCE PAGE
**************************************************************************************************/
import * as React from 'react';
import axios from 'axios';
import MenuLayout from '../layouts/menu-layout'
import { PlotWrapper, TableWrapper } from '../elements'

class DataScience extends React.Component {

    dataClean = require('../assets/images/data-clean.png')
    multihotDiagram = require('../assets/images/multihot.png')

    state = {
        dataHistory: [],
        votePlot: {},
        restrictedClassifiers: {},
        svmTune: [{
                'Hyper-Parameter': '-baseline-',
                'Best Value': '-', 
                'Accuracy': 54.2,
            }, {
                'Hyper-Parameter': 'learning_rate',
                'Best Value': 'invscaling', 
                'Accuracy': 58.5,
            }, {
                'Hyper-Parameter': 'eta0',
                'Best Value': '0.01', 
                'Accuracy': 59.5,
            }, {
                'Hyper-Parameter': 'power_t',
                'Best Value': '-', 
                'Accuracy': '-',
            }, {
                'Hyper-Parameter': 'max_iter',
                'Best Value': '200', 
                'Accuracy': 59.6,
            }, {
                'Hyper-Parameter': 'loss',
                'Best Value': 'epsilon_insensitive', 
                'Accuracy': 60.5,
            }, {
                'Hyper-Parameter': 'penalty (regularization)',
                'Best Value': '-', 
                'Accuracy': '-',
            }, {
                'Hyper-Parameter': 'class_weight',
                'Best Value': '-', 
                'Accuracy': '-',
            }, {
                'Hyper-Parameter': '-final-',
                'Best Value': '-', 
                'Accuracy': 60.5,
        }],
    }

    componentDidMount() {
        axios({
            url: 'api/recommend/data_history/',
            method: 'get',
        }).then( success => {
            //console.log(success.data);
            this.setState({dataHistory: success.data});
        }).catch( error => {
            console.log(error);
        });

        axios({
            url: 'api/recommend/score_plot/',
            method: 'get',
        }).then( success => {
            var jsonPlot = JSON.parse(success.data);
            this.setState({votePlot: jsonPlot});
        }).catch( error => {
            console.log(error);
        });

        axios({
            url: 'api/recommend/restricted_classifiers/',
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
                                It also shows for each source the percentage that is available of each feature.
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
                            <TableWrapper tableRows={ this.state.dataHistory } sizeClass='medium-plot'/>
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
                            </div>
                            <br></br>
                            <div>
                                The user score is the algorithm's target variable. 
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
                            <PlotWrapper plotConfig={ this.state.votePlot } sizeClass='small-plot' isStatic={ true } />
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
                                and then move to more complex models in search of higher accuracy or other metrics. 
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
                            <PlotWrapper plotConfig={ this.state.restrictedClassifiers } sizeClass='jumbo-plot' isStatic={ true }/>
                        </div>
                    </div>

                    <div className='pure-u-1'>
                        <div className='spacing-inner subheading'>
                            5] Tuning Support Vector Machine
                        </div>
                    </div>
                    <div className='pure-u-1-2'>
                        <div className='spacing-inner'>
                            <div>
                                The algorithm used is scikit-learn's&nbsp;
                                <a href='https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html' 
                                    className='link-format' target='blank_'>SVM Classifier</a>.
                                It can be tuned once the movies data has been updated, 
                                and a test user has scored many movies.
                                To tune the algorithm, a series of grid searches was run.
                                Each grid search only varied one hyper-parameter.
                                The list of hyper-parameters tested is shown in the adjacent table in order. 
                            </div>
                            <br></br>
                            <div>
                                Of course, its important to be strategic about the order in which the parameters are run. 
                                Generally, one starts with the learning rate, 
                                and reducing the number of trees/iterations to prevent overfitting.
                                Hyper-parameters run in the middle will vary with each algorithm. 
                                Towards the end, bring in regularization, 
                                as it is a finer correction term in the loss function.
                                Lastly, try class balancing methods. 
                                I keep these last because I've found they do not increase accuracy.
                            </div>
                            <br></br>
                            <div>
                                For each grid search of a hyper-parameter, at least 50 trials were run.
                                Each trial has a different seed, and produces its own best value.
                                The best value for a hyper-parameter is 
                                chosen as the most frequent best value among all the trials.
                                Each grid search is run using cross-validation with 5-folds, 
                                and the accuracy reported is the cross-validation test accuracy. 
                                Since cross-validation is used, a pipeline is in order to prevent data leakage.
                                The pipeline contains an imputer, a scaler, and an estimator. 
                            </div>
                        </div>
                    </div>
                    <div className='pure-u-1-2'>
                        <div className='spacing-inner small-font'>
                            <TableWrapper tableRows={ this.state.svmTune } sizeClass='small-plot'/>
                        </div>
                    </div>

                    <div className='pure-u-1'>
                        <div className='spacing-inner subheading'>
                            6] Conclusion
                        </div>
                    </div>
                    <div className='pure-u-1 pure-u-xl-1-2'>
                        <div className='spacing-inner'>
                            <div>
                                The tuned algorithm showed about 6% better accuracy over the baseline.
                                The algorithm then trains on each user's movie scores, 
                                and produces a model for that user.
                                The model then runs the movies the user hasn't score yet 
                                and its predictions are the movie recommendations.
                            </div>
                            <br></br>
                            <div>
                                We expect the "perceived accuracy" of each user's recommendations 
                                to vary from one user to another.
                                This is because each user will score movies differently,
                                and the algorithm will respond accordingly.
                                We also expect the accuracy to increase with the number of movies 
                                scored by the user, with at least a few hundred movies necessary 
                                for recommendations to be satisfactory.
                                This is because the algorithm, with the given features,&nbsp;
                                <u>is able to capture some ground truth</u> about
                                the user's taste in movies.
                            </div>
                        </div>
                    </div>
                    <div className='pure-u-1' style={{ height: '90px' }}></div>

                </div>
            </MenuLayout>
        );
    }
}

export default DataScience;
