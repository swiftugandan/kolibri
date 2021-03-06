<template>

  <CoreBase
    :authorized="$store.getters.userIsAuthorizedForCoach"
    authorizedRole="adminOrCoach"
    :showSubNav="false"
    v-bind="immersivePageProps"
  >
    <KPageContainer v-if="!loading">
      <h1>
        {{ quiz.title }}
      </h1>
      <p>
        {{ orderDescriptionString }}
      </p>

      <QuestionListPreview
        :fixedOrder="!quizIsRandomized"
        :readOnly="true"
        :selectedQuestions="selectedQuestions"
        :selectedExercises="selectedExercises"
      />
    </KPageContainer>
  </CoreBase>

</template>


<script>

  import fromPairs from 'lodash/fromPairs';
  import commonCoach from '../common';
  import QuestionListPreview from '../plan/CreateExamPage/QuestionListPreview';
  import { fetchQuizSummaryPageData } from '../plan/QuizSummaryPage/api';

  export default {
    name: 'ReportsQuizPreviewPage',
    components: {
      QuestionListPreview,
    },
    mixins: [commonCoach],
    data() {
      return {
        quiz: {
          assignments: [],
          learners_see_fixed_order: false,
          question_sources: [],
          title: '',
        },
        selectedExercises: {},
        loading: true,
      };
    },
    computed: {
      selectedQuestions() {
        return this.quiz.question_sources;
      },
      quizIsRandomized() {
        return !this.quiz.learners_see_fixed_order;
      },
      orderDescriptionString() {
        return this.quizIsRandomized
          ? this.coachStrings.$tr('orderRandomDescription')
          : this.coachStrings.$tr('orderFixedDescription');
      },
      immersivePageProps() {
        const title = this.$tr('pageTitle', { title: this.quiz.title });
        return {
          appBarTitle: title,
          pageTitle: title,
          immersivePage: true,
          immersivePageIcon: 'close',
          immersivePagePrimary: false,
          immersivePageRoute: this.$router.getRoute('ReportsQuizLearnerListPage'),
        };
      },
    },
    beforeRouteEnter(to, from, next) {
      // Use the same data-fetching as QuizSummaryPage to make sure we have
      // all of the Quiz and ContentNode data to render the preview
      return fetchQuizSummaryPageData(to.params.quizId)
        .then(data => {
          next(vm => vm.setData(data));
        })
        .catch(error => {
          next(vm => vm.setError(error));
        });
    },
    methods: {
      // @public
      setData(data) {
        const { exam, exerciseContentNodes } = data;
        this.quiz = exam;
        this.selectedExercises = fromPairs(exerciseContentNodes.map(x => [x.id, x]));
        this.loading = false;
        this.$store.dispatch('notLoading');
      },
      // @public
      setError(error) {
        this.$store.dispatch('handleApiError', error);
        this.loading = false;
        this.$store.dispatch('notLoading');
      },
    },
    $trs: {
      backToQuizAction: 'Back to quiz',
      pageTitle: `Preview of quiz '{title}'`,
    },
  };

</script>


<style lang="scss" scoped></style>
