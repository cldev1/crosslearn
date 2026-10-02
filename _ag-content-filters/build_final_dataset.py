import csv
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

VALID_TOPICS = {
    'strategy',
    'positioning',
    'discovery',
    'roadmaps-prioritization',
    'delivery-execution',
    'metrics-analytics',
    'leadership-org',
    'career-habits',
    'ai-product'
}

VALID_FORMATS = {
    'principle',
    'framework',
    'anti-pattern',
    'playbook'
}

# Explicit curated classifications for all 264 lessons
# Format: (format, [topics], source_slug)
# If source_slug is None, will be resolved from author string
CURATED = {
    # 01-18
    '01-ship-incomplete-bets': ('framework', ['strategy', 'ai-product'], 'lenny-rachitsky'),
    '02-delivery-includes-deprecation': ('principle', ['delivery-execution'], 'cat-wu'),
    '04-three-levels-of-product-work': ('framework', ['leadership-org', 'delivery-execution'], 'shreyas-doshi'),
    '05-eigenquestion': ('principle', ['strategy'], 'shreyas-doshi'),
    '06-explore-expand-extract': ('framework', ['strategy'], 'shreyas-doshi'),
    '07-steering-not-rowing': ('principle', ['strategy'], 'lenny-rachitsky'),
    '08-po-not-backlog-secretary': ('anti-pattern', ['delivery-execution', 'roadmaps-prioritization'], 'scrum-org'),
    '09-roadmap-70-20-10': ('framework', ['roadmaps-prioritization', 'strategy'], 'lenny-rachitsky'),
    '10-fourteen-pm-habits': ('playbook', ['career-habits'], 'lenny-rachitsky'),
    '11-strategy-between-vision-and-goals': ('framework', ['strategy'], 'lenny-rachitsky'),
    '12-ten-tests-for-pmf': ('playbook', ['strategy'], 'lenny-rachitsky'),
    '13-one-growth-lane': ('framework', ['strategy'], 'lenny-rachitsky'),
    '14-seven-lenses-for-an-idea': ('framework', ['strategy', 'discovery'], 'lenny-rachitsky'),
    '15-premortem-tigers': ('playbook', ['leadership-org'], 'shreyas-doshi'),
    '16-first-30-60-90': ('playbook', ['career-habits'], 'lenny-rachitsky'),
    '17-seven-discovery-paths': ('framework', ['discovery'], 'lenny-rachitsky'),
    '18-ic-to-pm-manager': ('principle', ['leadership-org', 'career-habits'], 'lenny-rachitsky'),

    # 19-37
    '19-ost-specific-stories': ('framework', ['discovery'], 'teresa-torres'),
    '20-okrs-vs-outcomes': ('principle', ['metrics-analytics'], 'teresa-torres'),
    '21-assumption-tests': ('playbook', ['discovery', 'delivery-execution'], 'teresa-torres'),
    '22-eight-metric-questions': ('playbook', ['metrics-analytics'], 'julie-zhuo'),
    '23-intuition-calendar': ('principle', ['career-habits', 'discovery'], 'julie-zhuo'),
    '24-prioritize-until-it-hurts': ('principle', ['roadmaps-prioritization', 'strategy'], 'julie-zhuo'),
    '25-gem-force-rank': ('framework', ['roadmaps-prioritization', 'metrics-analytics'], 'gibson-biddle'),
    '26-dhm-stack': ('framework', ['strategy', 'roadmaps-prioritization'], 'gibson-biddle'),
    '27-goals-then-evidence': ('framework', ['strategy', 'delivery-execution'], 'itamar-gilad'),
    '28-three-feature-buckets': ('framework', ['roadmaps-prioritization', 'strategy'], 'adam-nash'),
    '29-deconstruct-assumptions': ('playbook', ['discovery', 'delivery-execution'], 'teresa-torres'),
    '30-five-data-values': ('framework', ['metrics-analytics'], 'julie-zhuo'),
    '31-advisor-vs-solver': ('framework', ['leadership-org'], 'julie-zhuo'),
    '32-glee-vision': ('framework', ['strategy'], 'gibson-biddle'),
    '33-dhm-consumer-vs-b2b': ('framework', ['strategy'], 'gibson-biddle'),
    '34-invisible-product-work': ('principle', ['strategy', 'delivery-execution'], 'gibson-biddle'),
    '35-reward-killing-ideas': ('principle', ['leadership-org', 'delivery-execution'], 'itamar-gilad'),
    '36-po-not-full-time-backlog': ('anti-pattern', ['leadership-org', 'roadmaps-prioritization'], 'itamar-gilad'),
    '37-false-predictability': ('anti-pattern', ['roadmaps-prioritization', 'delivery-execution'], 'itamar-gilad'),

    # 38-60
    '38-discard-one-right-way': ('principle', ['strategy', 'career-habits'], 'shreyas-doshi'),
    '39-execution-as-wounds': ('anti-pattern', ['leadership-org', 'strategy'], 'shreyas-doshi'),
    '40-opposite-can-be-good': ('principle', ['strategy'], 'shreyas-doshi'),
    '41-roadmaps-never-stand-alone': ('anti-pattern', ['roadmaps-prioritization', 'strategy'], 'john-cutler'),
    '42-timeline-is-assumptions': ('anti-pattern', ['roadmaps-prioritization', 'strategy'], 'janna-bastow'),
    '43-enterprise-pm-cost-center': ('anti-pattern', ['leadership-org', 'strategy'], 'melissa-perri'),
    '44-okrs-need-strategy': ('anti-pattern', ['strategy', 'metrics-analytics'], 'john-cutler'),
    '45-product-then-project': ('principle', ['strategy', 'delivery-execution'], 'shreyas-doshi'),
    '46-strategy-names-tradeoffs': ('framework', ['strategy', 'metrics-analytics'], 'shreyas-doshi'),
    '47-smuggle-outcome-language': ('playbook', ['strategy', 'delivery-execution'], 'john-cutler'),
    '48-no-discovery-delivery-kingdoms': ('anti-pattern', ['delivery-execution', 'discovery'], 'john-cutler'),
    '49-operator-craftsperson-visionary': ('framework', ['career-habits', 'leadership-org'], 'shreyas-doshi'),
    '50-builder-tuner-innovator': ('framework', ['leadership-org', 'career-habits'], 'shreyas-doshi'),
    '51-data-not-trust-proxy': ('principle', ['metrics-analytics', 'leadership-org'], 'john-cutler'),
    '52-map-shapes-of-work': ('framework', ['delivery-execution', 'strategy'], 'john-cutler'),
    '53-branching-roadmaps': ('framework', ['roadmaps-prioritization'], 'pavel-samsonov'),
    '54-dual-track-not-cherry-pick': ('anti-pattern', ['delivery-execution', 'discovery'], 'pawel-huryn'),
    '55-stories-3cs-invest': ('framework', ['delivery-execution'], 'pawel-huryn'),
    '56-cpsr-the-problem': ('framework', ['discovery', 'strategy'], 'shreyas-doshi'),
    '57-seven-things-you-know': ('playbook', ['discovery', 'delivery-execution'], 'shreyas-doshi'),
    '58-research-refine-loop': ('anti-pattern', ['discovery'], 'shreyas-doshi'),
    '59-one-process-cannot-cover': ('framework', ['delivery-execution'], 'john-cutler'),
    '60-fewer-pdms-more-thinking': ('principle', ['leadership-org', 'roadmaps-prioritization'], 'john-cutler'),

    # 61-90
    '61-boat-go-faster': ('principle', ['strategy', 'roadmaps-prioritization'], 'shreyas-doshi'),
    '62-why-where-when': ('framework', ['strategy', 'delivery-execution'], 'pavel-samsonov'),
    '63-proxies-not-research': ('anti-pattern', ['discovery'], 'pavel-samsonov'),
    '64-skier-lags-double-diamond': ('framework', ['discovery', 'leadership-org'], 'pavel-samsonov'),
    '65-prio-is-strategy': ('principle', ['roadmaps-prioritization', 'strategy'], 'shreyas-doshi'),
    '66-good-vs-great-pm': ('principle', ['career-habits', 'strategy'], 'shreyas-doshi'),
    '67-b2b-strategy-tests': ('playbook', ['strategy'], 'shreyas-doshi'),
    '68-visualize-work-power': ('principle', ['leadership-org', 'delivery-execution'], 'john-cutler'),
    '69-impact-execution-strategy-market': ('framework', ['strategy', 'delivery-execution'], 'shreyas-doshi'),
    '70-ten-pm-commandments': ('playbook', ['career-habits', 'leadership-org'], 'shreyas-doshi'),
    '71-sell-doing-research': ('principle', ['discovery', 'leadership-org'], 'pavel-samsonov'),
    '72-hero-culture-spare-capacity': ('anti-pattern', ['leadership-org', 'delivery-execution'], 'pavel-samsonov'),
    '73-earn-team-trust': ('playbook', ['leadership-org'], 'john-cutler'),
    '74-bets-you-can-cut-short': ('anti-pattern', ['strategy', 'delivery-execution'], 'john-cutler'),
    '75-observe-first-research': ('principle', ['discovery'], 'pavel-samsonov'),
    '76-pm-work-is-private': ('anti-pattern', ['leadership-org', 'career-habits'], 'john-cutler'),
    '77-preventable-problem-paradox': ('anti-pattern', ['leadership-org'], 'shreyas-doshi'),
    '78-sprints-for-learning': ('principle', ['delivery-execution'], 'john-cutler'),
    '79-strategy-culture-execution-questions': ('playbook', ['strategy', 'leadership-org'], 'shreyas-doshi'),
    '80-messy-local-experiments': ('principle', ['delivery-execution', 'leadership-org'], 'john-cutler'),
    '81-north-star-thirty-percent': ('principle', ['strategy', 'discovery'], 'pavel-samsonov'),
    '82-measure-under-uncertainty': ('principle', ['metrics-analytics'], 'john-cutler'),
    '83-drivers-constraints-floats': ('framework', ['roadmaps-prioritization', 'delivery-execution'], 'john-cutler'),
    '84-we-might-be-wrong': ('anti-pattern', ['roadmaps-prioritization', 'discovery'], 'pavel-samsonov'),
    '85-produce-organize-self-promote': ('framework', ['leadership-org', 'career-habits'], 'shreyas-doshi'),
    '86-crossover-x-pattern': ('framework', ['strategy', 'leadership-org'], 'shreyas-doshi'),
    '87-ten-health-signals': ('playbook', ['leadership-org', 'delivery-execution'], 'john-cutler'),
    '88-ceo-test': ('playbook', ['strategy', 'leadership-org'], 'shreyas-doshi'),
    '89-gorilla-taxes': ('framework', ['strategy'], 'shreyas-doshi'),
    '90-product-vs-Product': ('principle', ['strategy', 'leadership-org'], 'shreyas-doshi'),

    # 91-120
    '91-ten-cognitive-biases': ('framework', ['career-habits', 'leadership-org'], 'shreyas-doshi'),
    '92-start-with-principles': ('playbook', ['strategy', 'leadership-org'], 'shreyas-doshi'),
    '93-four-team-modes': ('framework', ['delivery-execution', 'leadership-org'], 'shreyas-doshi'),
    '94-execution-is-often-strategy': ('anti-pattern', ['strategy', 'leadership-org'], 'shreyas-doshi'),
    '95-direction-plus-autonomy': ('framework', ['leadership-org'], 'pavel-samsonov'),
    '96-hostile-pm-environment': ('anti-pattern', ['leadership-org'], 'john-cutler'),
    '97-less-x-more-y': ('framework', ['career-habits', 'leadership-org'], 'shreyas-doshi'),
    '98-inputs-execution-outputs-outcomes': ('framework', ['metrics-analytics', 'delivery-execution'], 'shreyas-doshi'),
    '99-pm-team-member-not-mini-ceo': ('playbook', ['leadership-org', 'career-habits'], 'john-cutler'),
    '100-proxy-delusion': ('anti-pattern', ['metrics-analytics'], 'shreyas-doshi'),
    '101-positioning-five-components': ('framework', ['positioning'], 'april-dunford'),
    '102-category-assumptions': ('principle', ['positioning'], 'april-dunford'),
    '103-loose-then-tight-positioning': ('principle', ['positioning'], 'april-dunford'),
    '104-sell-market-pov': ('principle', ['positioning'], 'april-dunford'),
    '105-seven-virality-strategies': ('framework', ['strategy', 'discovery'], 'lenny-rachitsky'),
    '106-feature-factory-vs-inventing': ('anti-pattern', ['delivery-execution', 'leadership-org'], 'itamar-gilad'),
    '107-results-strategy-initiative-leadership': ('framework', ['strategy', 'leadership-org'], 'gibson-biddle'),
    '108-transform-vs-streamline': ('framework', ['strategy'], 'melissa-perri'),
    '109-product-thinking-solution-shape': ('principle', ['strategy', 'delivery-execution'], 'melissa-perri'),
    '110-designer-pushback-user-language': ('playbook', ['leadership-org', 'discovery'], 'julie-zhuo'),
    '111-high-agency': ('principle', ['career-habits'], 'shreyas-doshi'),
    '112-nine-time-principles-lno': ('framework', ['career-habits'], 'shreyas-doshi'),
    '113-opportunity-cost-not-roi': ('principle', ['strategy', 'career-habits'], 'shreyas-doshi'),
    '114-radical-delegation': ('playbook', ['leadership-org', 'career-habits'], 'shreyas-doshi'),
    '115-10-30-50-pm': ('framework', ['career-habits', 'leadership-org'], 'shreyas-doshi'),
    '116-eyeglass-store': ('principle', ['career-habits', 'discovery'], 'shreyas-doshi'),
    '117-curse-of-brilliance': ('anti-pattern', ['career-habits', 'leadership-org'], 'shreyas-doshi'),
    '118-messy-middle-inputs': ('framework', ['metrics-analytics', 'strategy'], 'john-cutler'),
    '119-change-the-words': ('framework', ['strategy', 'roadmaps-prioritization'], 'john-cutler'),
    '120-primary-user-benefit': ('framework', ['strategy', 'positioning'], 'pavel-samsonov'),

    # 121-150
    '121-positioning-before-story': ('principle', ['positioning'], 'april-dunford'),
    '122-position-competitors': ('principle', ['positioning'], 'april-dunford'),
    '123-perf-scope-times-impact': ('framework', ['career-habits', 'leadership-org'], 'itamar-gilad'),
    '124-cd-is-business-practice': ('principle', ['delivery-execution'], 'janna-bastow'),
    '125-oceans-11-cascade': ('framework', ['strategy', 'roadmaps-prioritization'], 'lenny-rachitsky'),
    '126-family-to-dream-team': ('framework', ['leadership-org'], 'gibson-biddle'),
    '127-ab-swing-for-the-fence': ('principle', ['metrics-analytics', 'discovery'], 'teresa-torres'),
    '128-designer-answers-pm-pushback': ('framework', ['leadership-org', 'delivery-execution'], 'julie-zhuo'),
    '129-ship-design-product-business': ('framework', ['strategy', 'delivery-execution'], 'des-traynor'),
    '130-proof-of-worth': ('anti-pattern', ['career-habits', 'leadership-org'], 'shreyas-doshi'),
    '131-climb-the-loops': ('framework', ['leadership-org', 'career-habits'], 'pavel-samsonov'),
    '132-metrics-are-not-goals': ('principle', ['metrics-analytics'], 'pavel-samsonov'),
    '133-artifact-is-the-conversation': ('principle', ['leadership-org', 'discovery'], 'pavel-samsonov'),
    '134-outcome-first-planning': ('framework', ['metrics-analytics', 'roadmaps-prioritization'], 'pavel-samsonov'),
    '135-congruence-quality-timing': ('framework', ['roadmaps-prioritization', 'leadership-org'], 'john-cutler'),
    '136-three-roadmaps': ('framework', ['roadmaps-prioritization', 'leadership-org'], 'melissa-perri'),
    '137-vision-strategy-positioning-clocks': ('framework', ['positioning', 'strategy'], 'april-dunford'),
    '138-timeline-vicious-cycle': ('anti-pattern', ['roadmaps-prioritization', 'delivery-execution'], 'janna-bastow'),
    '139-foundation-not-big-bang': ('anti-pattern', ['strategy', 'delivery-execution'], 'john-cutler'),
    '140-segment-then-champion': ('principle', ['positioning', 'discovery'], 'april-dunford'),
    '141-fidelity-of-thinking': ('principle', ['delivery-execution', 'discovery'], 'pavel-samsonov'),
    '142-absolute-not-relative': ('principle', ['positioning', 'strategy'], 'pavel-samsonov'),
    '143-low-hanging-fruit': ('anti-pattern', ['roadmaps-prioritization'], 'pavel-samsonov'),
    '144-design-documents-decisions': ('principle', ['delivery-execution', 'discovery'], 'pavel-samsonov'),
    '145-company-vs-product-positioning': ('framework', ['positioning', 'strategy'], 'april-dunford'),
    '146-positioning-misalignment-catch-22': ('anti-pattern', ['positioning', 'roadmaps-prioritization'], 'april-dunford'),
    '147-eight-first-time-leader-mistakes': ('anti-pattern', ['leadership-org'], 'melissa-perri'),
    '148-org-vs-swimlane-smt': ('framework', ['strategy', 'leadership-org'], 'gibson-biddle'),
    '149-simplicity-is-a-tactic': ('principle', ['delivery-execution', 'strategy'], 'john-cutler'),
    '150-value-exchange-rate': ('principle', ['leadership-org', 'metrics-analytics'], 'julie-zhuo'),

    # 151-180
    '151-deadlines-not-the-incentive': ('principle', ['roadmaps-prioritization', 'leadership-org'], 'janna-bastow'),
    '152-burnout-black-box': ('anti-pattern', ['career-habits', 'leadership-org'], 'john-cutler'),
    '153-wean-off-nps': ('playbook', ['metrics-analytics'], 'john-cutler'),
    '154-metrics-from-guessing-the-build': ('anti-pattern', ['metrics-analytics'], 'pavel-samsonov'),
    '155-not-the-main-character': ('principle', ['discovery'], 'pavel-samsonov'),
    '156-bake-in-the-expertise': ('playbook', ['leadership-org', 'delivery-execution'], 'melissa-perri'),
    '157-influence-execs-how-judged': ('principle', ['leadership-org'], 'melissa-perri'),
    '158-disappointment-is-expectations': ('principle', ['leadership-org'], 'julie-zhuo'),
    '159-stop-deciphering-the-ceo': ('principle', ['leadership-org'], 'shreyas-doshi'),
    '160-real-alternatives-not-theoretical': ('principle', ['positioning'], 'april-dunford'),
    '161-three-bullets-on-the-slide': ('anti-pattern', ['roadmaps-prioritization', 'leadership-org'], 'john-cutler'),
    '162-idle-beats-feasible-code': ('principle', ['delivery-execution', 'strategy'], 'pavel-samsonov'),
    '163-storyboards-not-hifi': ('playbook', ['discovery', 'delivery-execution'], 'pavel-samsonov'),
    '164-five-things-starting-in-product': ('playbook', ['career-habits', 'leadership-org'], 'melissa-perri'),
    '165-considered-purchase-no-decision': ('principle', ['positioning'], 'april-dunford'),
    '166-category-orients-value-story': ('framework', ['positioning'], 'april-dunford'),
    '167-three-value-themes': ('principle', ['positioning'], 'april-dunford'),
    '168-walkthrough-five-moves': ('playbook', ['positioning'], 'april-dunford'),
    '169-just-talk-to-customers-cop-out': ('anti-pattern', ['positioning', 'discovery'], 'april-dunford'),
    '170-champion-then-arm': ('playbook', ['positioning'], 'april-dunford'),
    '171-same-value-same-positioning': ('principle', ['positioning', 'strategy'], 'april-dunford'),
    '172-position-against-approaches': ('principle', ['positioning'], 'april-dunford'),
    '173-storytelling-maps-approaches': ('framework', ['positioning'], 'april-dunford'),
    '174-hoard-giant-ghost': ('framework', ['positioning'], 'april-dunford'),
    '175-methods-need-inputs': ('anti-pattern', ['leadership-org', 'delivery-execution'], 'pavel-samsonov'),
    '176-ux-not-the-screen': ('principle', ['discovery', 'delivery-execution'], 'pavel-samsonov'),
    '177-go-faster-define-value': ('principle', ['delivery-execution'], 'john-cutler'),
    '178-exec-never-seen-a-flop': ('anti-pattern', ['leadership-org'], 'john-cutler'),
    '179-working-with-developers': ('playbook', ['delivery-execution', 'leadership-org'], 'john-cutler'),
    '180-presentation-culture-fallacies': ('anti-pattern', ['leadership-org'], 'john-cutler'),

    # 181-200
    '181-devalued-not-a-seat': ('anti-pattern', ['leadership-org', 'career-habits'], 'john-cutler'),
    '182-leadership-defaults': ('framework', ['leadership-org'], 'john-cutler'),
    '183-new-senior-leaders': ('anti-pattern', ['leadership-org'], 'john-cutler'),
    '184-pyramids-vs-orbits': ('framework', ['strategy', 'leadership-org'], 'john-cutler'),
    '185-manager-roles-converge': ('framework', ['leadership-org', 'career-habits'], 'julie-zhuo'),
    '186-interview-questions': ('playbook', ['leadership-org'], 'julie-zhuo'),
    '187-keep-positioning-loose': ('principle', ['positioning'], 'april-dunford'),
    '188-b2b-fear-no-decision': ('principle', ['positioning'], 'april-dunford'),
    '189-decision-making-documentation': ('playbook', ['leadership-org', 'delivery-execution'], 'pavel-samsonov'),
    '190-work-with-not-for': ('principle', ['leadership-org', 'delivery-execution'], 'pavel-samsonov'),
    '191-demo-context-then-value': ('playbook', ['positioning'], 'april-dunford'),
    '192-not-xyz-positioning': ('anti-pattern', ['positioning'], 'april-dunford'),
    '193-satisfaction-not-a-metric': ('anti-pattern', ['metrics-analytics'], 'pavel-samsonov'),
    '194-definition-of-good-hiring': ('playbook', ['leadership-org'], 'pavel-samsonov'),
    '195-not-catering-to-wants': ('framework', ['discovery', 'strategy'], 'pavel-samsonov'),
    '196-capture-inputs-propagate': ('playbook', ['delivery-execution', 'leadership-org'], 'pavel-samsonov'),
    '197-no-single-safe-alternative': ('anti-pattern', ['delivery-execution', 'leadership-org'], 'melissa-perri'),
    '198-renaming-pms-hurts-hiring': ('anti-pattern', ['leadership-org'], 'melissa-perri'),
    '199-specific-ask': ('playbook', ['leadership-org'], 'julie-zhuo'),
    '200-experts-vs-armchair': ('framework', ['career-habits'], 'julie-zhuo'),

    # 201-225
    '201-first-strategy-doc-alignment': ('framework', ['strategy', 'leadership-org'], 'george-nurijanian'),
    '202-tech-debt-first-30-days': ('playbook', ['delivery-execution', 'leadership-org'], 'george-nurijanian'),
    '203-merit-vs-corporate-rewards': ('principle', ['career-habits', 'leadership-org'], 'george-nurijanian'),
    '204-customer-driven-content': ('playbook', ['discovery', 'positioning'], 'alejandro-vivanco'),
    '205-growth-wom-brand-dogfood': ('framework', ['strategy'], 'grant-lee'),
    '206-inputs-chat-outputs': ('framework', ['ai-product'], 'jason-spielman'),
    '207-unsolicited-affection-pmf': ('principle', ['metrics-analytics', 'discovery'], 'guillermo-rauch'),
    '208-early-stage-sales-learnings': ('playbook', ['discovery', 'positioning'], 'jen-abel'),
    '209-load-bearing-perspectives': ('framework', ['strategy', 'leadership-org'], 'nan-yu'),
    '210-customers-as-investors': ('principle', ['strategy'], 'martin-tobias'),
    '211-clarity-by-subtraction': ('principle', ['strategy', 'roadmaps-prioritization'], 'shreyas-doshi'),
    '212-shadow-of-doubt': ('principle', ['leadership-org'], 'george-nurijanian'),
    '213-ppf-then-mmf': ('framework', ['strategy', 'discovery'], 'sajith-pai'),
    '214-refinement-continuous-not-meeting': ('principle', ['delivery-execution'], 'scrum-org'),
    '215-ai-fluency-operating-model': ('framework', ['ai-product', 'leadership-org'], 'scrum-org'),
    '216-authorship-before-process': ('principle', ['leadership-org', 'delivery-execution'], 'scrum-org'),
    '217-strength-without-contempt': ('principle', ['leadership-org'], 'scrum-org'),
    '218-elevate-others-ambition': ('principle', ['leadership-org', 'career-habits'], 'lenny-rachitsky'),
    '219-unship-before-launch': ('playbook', ['ai-product', 'delivery-execution'], 'lenny-rachitsky'),
    '220-product-can-now': ('principle', ['ai-product', 'roadmaps-prioritization'], 'lenny-rachitsky'),
    '221-dont-ship-org-chart': ('anti-pattern', ['leadership-org', 'ai-product'], 'lenny-rachitsky'),
    '222-rejection-register': ('playbook', ['roadmaps-prioritization'], 'scrum-org'),
    '223-ai-path-not-answers': ('principle', ['ai-product', 'strategy'], 'shreyas-doshi'),
    '224-traits-that-matter-more': ('framework', ['leadership-org', 'career-habits'], 'shreyas-doshi'),
    '225-ai-wip-limits-review': ('playbook', ['delivery-execution', 'ai-product'], 'scrum-org'),

    # 226-265
    '226-stakeholder-dump-not-problem': ('anti-pattern', ['discovery', 'roadmaps-prioritization'], 'george-nurijanian'),
    '227-jtbd-without-forces': ('framework', ['discovery'], 'george-nurijanian'),
    '228-judgment-is-a-product': ('framework', ['career-habits', 'strategy'], 'george-nurijanian'),
    '229-issue-tree-before-features': ('framework', ['discovery', 'roadmaps-prioritization'], 'george-nurijanian'),
    '230-where-did-we-land': ('playbook', ['leadership-org', 'delivery-execution'], 'george-nurijanian'),
    '231-ai-agile-transformations-rhyme': ('anti-pattern', ['ai-product', 'leadership-org'], 'scrum-org'),
    '232-retros-format-not-the-problem': ('anti-pattern', ['delivery-execution'], 'scrum-org'),
    '233-factory-that-produces-ideas': ('anti-pattern', ['strategy', 'discovery'], 'george-nurijanian'),
    '234-verbalized-sampling-idea-diversity': ('playbook', ['discovery', 'ai-product'], 'george-nurijanian'),
    '235-reality-not-status-meeting': ('playbook', ['delivery-execution', 'leadership-org'], 'scrum-org'),
    '236-taste-knowing-when-to-stop': ('principle', ['career-habits', 'discovery'], 'lenny-rachitsky'),
    '237-use-case-map-before-ask-agent': ('framework', ['ai-product', 'discovery'], 'george-nurijanian'),
    '238-edge-cases-ahead-of-what-about': ('playbook', ['delivery-execution', 'leadership-org'], 'george-nurijanian'),
    '239-extract-domain-from-products': ('framework', ['discovery', 'strategy'], 'george-nurijanian'),
    '240-money-in-the-banana-stand': ('principle', ['strategy', 'metrics-analytics'], 'lenny-rachitsky'),
    '241-core-product-value-phrase-metrics': ('framework', ['positioning', 'metrics-analytics'], 'lenny-rachitsky'),
    '242-ideology-and-dris-over-coordination': ('principle', ['leadership-org', 'delivery-execution'], 'lenny-rachitsky'),
    '243-load-strongest-performers-first': ('principle', ['leadership-org'], 'lenny-rachitsky'),
    '244-evals-core-pm-craft': ('playbook', ['ai-product', 'delivery-execution'], 'lenny-rachitsky'),
    '245-cant-vibe-experimentation': ('anti-pattern', ['metrics-analytics', 'discovery'], 'george-nurijanian'),
    '246-opportunity-map-without-inventing': ('playbook', ['discovery'], 'george-nurijanian'),
    '247-critical-decision-method': ('playbook', ['discovery', 'career-habits'], 'george-nurijanian'),
    '248-problem-first-invert-bad-ideas': ('playbook', ['ai-product', 'strategy'], 'george-nurijanian'),
    '249-power-user-shift-frequency': ('principle', ['metrics-analytics'], 'george-nurijanian'),
    '250-ai-workflow-inventory': ('playbook', ['ai-product', 'delivery-execution'], 'scrum-org'),
    '251-metric-review-skills': ('playbook', ['metrics-analytics'], 'george-nurijanian'),
    '252-last-roadmap-durable-convictions': ('principle', ['roadmaps-prioritization', 'ai-product'], 'claire-vo'),
    '253-audience-empathy-map': ('framework', ['leadership-org', 'discovery'], 'shreyas-doshi'),
    '254-hallway-meeting-agrees': ('anti-pattern', ['leadership-org', 'delivery-execution'], 'scrum-org'),
    '255-velocity-without-design': ('anti-pattern', ['delivery-execution'], 'george-nurijanian'),
    '256-funeral-for-change': ('playbook', ['leadership-org'], 'molly-graham'),
    '257-ai-delegation-not-legos': ('principle', ['leadership-org', 'ai-product'], 'molly-graham'),
    '258-keep-judgment-taste-vision': ('principle', ['leadership-org', 'career-habits'], 'molly-graham'),
    '259-every-ic-is-now-a-manager': ('framework', ['leadership-org', 'career-habits'], 'molly-graham'),
    '260-three-pm-paths': ('framework', ['career-habits', 'leadership-org'], 'geoff-charles'),
    '261-good-product-work-is-thinking': ('principle', ['strategy', 'career-habits'], 'marty-cagan'),
    '262-ship-all-our-bad-ideas': ('anti-pattern', ['ai-product', 'delivery-execution'], 'claire-vo'),
    '263-pm-craft-is-decision-making': ('principle', ['career-habits', 'strategy'], 'ryan-stein'),
    '264-ask-when-confused': ('principle', ['career-habits', 'leadership-org'], 'molly-graham'),
    '265-friction-is-sometimes-the-learning': ('principle', ['career-habits', 'discovery'], 'molly-graham'),
}

print(f"Total curated lessons: {len(CURATED)}")

# Verification
dirs = [d for d in os.listdir('.') if re.match(r'^\d{2,3}-[a-z0-9-]+$', d, re.I)]
dirs.sort(key=lambda s: int(s.split('-')[0]))

assert set(dirs) == set(CURATED.keys()), f"Mismatch in slugs! Diff: {set(dirs) ^ set(CURATED.keys())}"

format_counts = Counter()
topic_counts = Counter()
source_counts = Counter()
errors = []

for slug, (fmt, topics, src) in CURATED.items():
    if fmt not in VALID_FORMATS:
        errors.append(f"[{slug}] Invalid format: {fmt}")
    format_counts[fmt] += 1

    if not isinstance(topics, list) or len(topics) < 1 or len(topics) > 2:
        errors.append(f"[{slug}] Invalid topics count: {topics}")
    for t in topics:
        if t not in VALID_TOPICS:
            errors.append(f"[{slug}] Invalid topic: {t}")
        topic_counts[t] += 1

    if not src or not re.match(r'^[a-z0-9-]+$', src):
        errors.append(f"[{slug}] Invalid source slug: {src}")
    source_counts[src] += 1

if errors:
    print(f"FAILED WITH {len(errors)} ERRORS:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print("\n=== FORMAT DISTRIBUTION ===")
for f_name, count in format_counts.most_common():
    pct = (count / len(CURATED)) * 100
    print(f"  {f_name:15}: {count:3} ({pct:5.1f}%)")

print("\n=== TOPIC DISTRIBUTION ===")
for t_name, count in topic_counts.most_common():
    pct = (count / len(CURATED)) * 100
    print(f"  {t_name:25}: {count:3} ({pct:5.1f}%)")

print("\n=== SOURCE DISTRIBUTION ===")
for s_name, count in source_counts.most_common():
    pct = (count / len(CURATED)) * 100
    print(f"  {s_name:25}: {count:3} ({pct:5.1f}%)")

# Write out the updated draft-tags.csv
with open('_ag-content-filters/draft-tags.csv', encoding='utf-8') as f:
    orig_rows = list(csv.DictReader(f))

updated_rows = []
for r in orig_rows:
    slug = r['slug']
    fmt, topics, src = CURATED[slug]
    r['format'] = fmt
    r['topics'] = ';'.join(topics)
    r['source_slug'] = src
    updated_rows.append(r)

with open('_ag-content-filters/draft-tags.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['slug', 'title', 'source_author', 'source_slug', 'format', 'topics', 'file_type'])
    writer.writeheader()
    writer.writerows(updated_rows)

print("\nSuccessfully updated _ag-content-filters/draft-tags.csv with final curated tags.")

