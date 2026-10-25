import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
import pingouin as pg
import pandas as pd
import random


def map_experience(snip_df, raw_df):
    sample = snip_df.groupby('response_id', group_keys=True).readability_numeric.count()
    desc = raw_df[['Response ID',
                   'Which of the following best describes the level of your expertise with the Java programming language?',
                   'How many years of professional coding experience do you have, including any internships during your education?']]
    desc.columns = ['response_id', 'experience', 'years']

    sample = sample.reset_index().merge(desc, on='response_id')
    exp_coding = {
        'Intermediate: I have a strong understanding of Java programming and can work on complex projects': 'Intermediate',
        'Advanced: I have extensive experience with Java programming and consider myself highly proficient in the language': 'Advanced',
        'Beginner: I have some experience with Java programming and can write basic programs': 'Beginner'}

    sample.experience = sample.experience.replace(exp_coding)

    exp_mapping = {'Beginner': [{'Beginner': ['1–2 years', '3–4 years', 'Less than 1 year']},
                                {'Intermediate': ['Less than 1 year']}, ],

                   'Intermediate': [
                       {'Intermediate': ['1–2 years', '3–4 years', '7–8 years', '5–6 years', '9–10 years']},
                       {'Advanced': ['1–2 years', 'Less than 1 year']},
                       {'Beginner': ['7–8 years', '5–6 years', '9–10 years', 'More than 10 years']}],

                   'Advanced': [
                       {'Advanced': ['3–4 years', '7–8 years', '5–6 years', '9–10 years', 'More than 10 years']},
                       {'Intermediate': ['More than 10 years']}]}

    sample['fixed_experience'] = None
    for level in exp_mapping.keys():
        # print(level, len(sample[(sample.experience == level)]))
        level_desc = exp_mapping[level]
        for one_level_desc in level_desc:
            for reported_level, years in one_level_desc.items():
                sample.loc[(sample.experience == reported_level) &
                           (sample.years.isin(years)), 'fixed_experience'] = level

    # sample[sample.experience != sample.fixed_experience]

    return sample


def calculate_icc_for_scales(snip_df):
    factors = ['short', 'top_bottom', 'sufficient_info', 'clear_goal', 'basic',
               'logical_separation', 'flat', 'action_per_line', 'constants', 'naming',
               'style_guide', 'balance']

    for model in factors[:-1]:
        new_format = []
        for sid in snip_df.snip_id.unique():
            row = random.sample(snip_df.loc[snip_df.snip_id == sid, model].tolist(), 10)
            row.append(sid)
            new_format.append(row)

        new_format = pd.DataFrame(new_format,
                                  columns=['r1', 'r2', 'r3', "r4", 'r5', 'r6', "r7", 'r8', 'r9', 'r10', 'snip_id'])
        new_format = new_format.melt(id_vars='snip_id')

        icc = pg.intraclass_corr(data=new_format, targets='snip_id', raters='variable',
                                 ratings='value', nan_policy='omit').round(3)
        print(f'ICC for scale {model}: {icc.iloc[0, 2]}')


def calculate_percent_agreement(df):
    b = df.readable * (df.readable - 1) + df.unreadable * (df.unreadable - 1)
    c = (df.readable + df.unreadable) * (df.readable + df.unreadable - 1)
    percent_agreement = (b / c).mean()
    return percent_agreement


def beatiful_point_plot(point_plot_df):
    sns.set_context("talk")
    x_value_mapping = {
        'short': 'Code\nLength',
        'top_bottom': 'Reading\nFlow',
        'sufficient_info': 'Contextual\nInfo*',
        'clear_goal': 'Clear\nGoal',
        'basic': 'Code\nPatterns',
        'logical_separation': 'Code\nStructure',
        'flat': 'Nesting',
        'action_per_line': 'Inline\nActions',
        'constants': 'Magic\nNumbers',
        'naming': 'Naming',
        'style_guide': 'Code\nStyle',
        'balance': 'Visual\nOrganization\n'
    }

    plt.figure(figsize=(20, 10))
    sns.pointplot(data=point_plot_df, x="variable", y="value", hue='summ_readability')

    plt.xticks(
        ticks=range(len(x_value_mapping)),
        labels=[x_value_mapping[label] for label in x_value_mapping]
    )

    y_tick_positions = [-1, 0, 1]
    y_tick_labels = ['Unreadable', 'Neutral', 'Readable']
    plt.yticks(y_tick_positions, y_tick_labels)

    plt.xlabel('Code Readability Aspect')
    plt.ylabel('Readability Pole')

    custom_legend_labels = ['Unreadable', 'Readable', 'Ambiguous']
    legend_elements = [Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=label)
                       for color, label in zip(sns.color_palette(), custom_legend_labels)]

    plt.legend(handles=legend_elements, title="Snippets'\nReadability")

    plt.savefig('images/CRval.pdf', dpi=1200, bbox_inches='tight')

    plt.show()


def aggregate_readability(snip_df, neutral_threshold=0.1):
    snippets_table = snip_df.pivot_table(index='snip_id', columns='readability_numeric', values='response_id',
                                         aggfunc='count')
    snippets_table.columns = ['unreadable', 'readable']
    snippets_table = snippets_table.reset_index()
    snippets_table = snippets_table.fillna(0)
    snippets_table['diff1'] = ((snippets_table.unreadable / snippets_table.readable) - 1) ** 2
    snippets_table['diff2'] = abs(snippets_table.unreadable - snippets_table.readable) / (
                snippets_table.unreadable + snippets_table.readable)
    snippets_table = snippets_table.sort_values(by='diff2', ascending=False)
    snippets_table['readability'] = snippets_table.readable > snippets_table.unreadable
    snippets_table['neutral'] = False
    snippets_table.loc[snippets_table.diff2 < neutral_threshold, 'neutral'] = True

    return snippets_table


def clear_bad_respondents(snip_df, top=4):
    t = (snip_df.groupby('response_id').readability_numeric.sum() == 0)
    negative_guys = t[t].index.tolist()
    negative_guys_df = snip_df[snip_df.response_id.isin(negative_guys)]
    negative_guys_final = (negative_guys_df.response_id.value_counts()
                           .sort_values(ascending=False).head(top).index.tolist())
    snip_df = snip_df[~snip_df.response_id.isin(negative_guys_final)]

    return snip_df