<template>

  <div :style="{ backgroundColor: $coreBgLight }">
    <h3 class="header">
      {{ $tr('header') }}
    </h3>

    <ul ref="attemptList" class="history-list">
      <template v-for="(attemptLog, index) in attemptLogs">
        <li
          :key="index"
          class="clickable attempt-item"
          :style="{
            borderBottom: `2px solid ${$coreTextDisabled}`,
            backgroundColor: isSelected(index) ? $coreTextDisabled : '',
          }"
          @click="setSelectedAttemptLog(index)"
        >
          <div class="title">
            <mat-svg
              v-if="attemptLog.noattempt"
              class="item svg-item"
              :style=" { fill: $coreTextAnnotation }"
              category="navigation"
              name="cancel"
            />
            <mat-svg
              v-else-if="attemptLog.correct"
              class="item svg-item"
              :style="{ fill: $coreStatusCorrect }"
              category="action"
              name="check_circle"
            />
            <mat-svg
              v-else-if="attemptLog.error"
              class="svg-item"
              :style=" { fill: $coreTextAnnotation }"
              category="alert"
              name="error_outline"
            />
            <mat-svg
              v-else-if="!attemptLog.correct"
              class="item svg-item"
              :style="{ fill: $coreStatusWrong }"
              category="navigation"
              name="cancel"
            />
            <mat-svg
              v-else-if="attemptLog.hinted"
              class="item svg-item"
              :style=" { fill: $coreTextAnnotation }"
              category="action"
              name="lightbulb_outline"
            />
            <h3 class="item">
              {{ $tr('question', {questionNumber: attemptLog.questionNumber}) }}
            </h3>
          </div>
          <CoachContentLabel
            class="coach-content-label"
            :value="attemptLog.num_coach_contents || 0"
            :isTopic="false"
          />
        </li>
      </template>
    </ul>
  </div>

</template>


<script>

  import themeMixin from 'kolibri.coreVue.mixins.themeMixin';
  import CoachContentLabel from 'kolibri.coreVue.components.CoachContentLabel';

  export default {
    name: 'AttemptLogList',
    components: {
      CoachContentLabel,
    },
    mixins: [themeMixin],
    props: {
      attemptLogs: {
        type: Array,
        required: true,
      },
      selectedQuestionNumber: {
        type: Number,
        required: true,
      },
    },
    mounted() {
      this.$nextTick(() => {
        this.scrollToSelectedAttemptLog(this.selectedQuestionNumber);
      });
    },
    methods: {
      setSelectedAttemptLog(questionNumber) {
        this.$emit('select', questionNumber);
        this.scrollToSelectedAttemptLog(questionNumber);
      },
      isSelected(questionNumber) {
        return Number(this.selectedQuestionNumber) === questionNumber;
      },
      scrollToSelectedAttemptLog(questionNumber) {
        const selectedElement = this.$refs.attemptList.children[questionNumber];
        if (selectedElement) {
          const parent = this.$el.parentElement;
          parent.scrollTop =
            selectedElement.offsetHeight * (questionNumber + 1) - parent.offsetHeight / 2;
        }
      },
    },
    $trs: {
      header: 'Answer history',
      today: 'Today',
      yesterday: 'Yesterday',
      daysAgo: '{ daysElapsed } days ago',
      question: 'Question { questionNumber, number }',
    },
  };

</script>


<style lang="scss" scoped>

  .title {
    display: inline-block;
  }

  .coach-content-label {
    display: inline-block;
    margin-left: 8px;
    vertical-align: middle;
  }

  .header {
    padding-top: 10px;
    padding-bottom: 10px;
    padding-left: 20px;
    margin: 0;
  }

  .history-list {
    max-height: inherit;
    padding-left: 0;
    margin: 0;
    list-style-type: none;
  }

  .item {
    display: inline-block;
    height: 24px;
  }

  .svg-item {
    width: 32px;
    height: auto;
    margin-right: 8px;
    vertical-align: middle;
  }

  .attempt-item {
    display: block;
    min-width: 120px;
    padding-left: 20px;
    clear: both;
  }

  .clickable {
    display: block;
    cursor: pointer;
  }

</style>
