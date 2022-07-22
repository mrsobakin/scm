
base_url = "https://edu.sirius.online/#/course"

knowledge_areas = {
    1: "Математика",
    2: "Программирование",
    3: "Лингвистика",
    4: "Физика",
    5: "Химия",
    6: "Биология"
}

# ~ metrics_minmax = {1: {'avg_try_count': (1.25, 9.689423076923076), 'done_rate_by_media': (0.767865539632781, 0.2964470238516526), 'done_rate_by_prev_element_metric': (1.0, 0.6757257971238), 'done_rate_by_pupils': (1.0, 0.7962962962962963), 'done_in_first_try_rate_metric': (0.9436078006500541, 0.4620065789473684), 'avg_solve_improvement_time_metric': (0.6801716583333335, 39.760632186666655), 'number_of_module_students_infometric': (64.05, 3002.5999999999995), 'achieved_in_module_number_infometric': (42.0, 1484.3999999999999), 'module_conversion_metric': (0.9892840329171609, 0.633298718670797), 'mean_module_score_metric': (0.9577698219972708, 0.606524006722232), 'module_done_rate_metric': (0.97735924634671, 0.47473193473193465), 'module_drop_on_rate_metric': (0.00186112814115757, 0.34964438122332847), 'time_spent_metric': (0.0, 1.0), 'number_of_students_infometric': (1561.1, 7478.699999999999), 'cert_rate_among_nontransfered_metric': (0.4038245904025281, 0.05420833333333327)}, 2: {'avg_try_count': (1.25, 9.689423076923076), 'done_rate_by_media': (0.767865539632781, 0.2964470238516526), 'done_rate_by_prev_element_metric': (1.0, 0.6757257971238), 'done_rate_by_pupils': (1.0, 0.7962962962962963), 'done_in_first_try_rate_metric': (0.9436078006500541, 0.4620065789473684), 'avg_solve_improvement_time_metric': (0.6801716583333335, 39.760632186666655), 'number_of_module_students_infometric': (64.05, 3002.5999999999995), 'achieved_in_module_number_infometric': (42.0, 1484.3999999999999), 'module_conversion_metric': (0.9892840329171609, 0.633298718670797), 'mean_module_score_metric': (0.9577698219972708, 0.606524006722232), 'module_done_rate_metric': (0.97735924634671, 0.47473193473193465), 'module_drop_on_rate_metric': (0.00186112814115757, 0.34964438122332847), 'time_spent_metric': (0.0, 1.0), 'number_of_students_infometric': (1561.1, 7478.699999999999), 'cert_rate_among_nontransfered_metric': (0.4038245904025281, 0.05420833333333327)}, 3: {'avg_try_count': (1.25, 9.689423076923076), 'done_rate_by_media': (0.767865539632781, 0.2964470238516526), 'done_rate_by_prev_element_metric': (1.0, 0.6757257971238), 'done_rate_by_pupils': (1.0, 0.7962962962962963), 'done_in_first_try_rate_metric': (0.9436078006500541, 0.4620065789473684), 'avg_solve_improvement_time_metric': (0.6801716583333335, 39.760632186666655), 'number_of_module_students_infometric': (64.05, 3002.5999999999995), 'achieved_in_module_number_infometric': (42.0, 1484.3999999999999), 'module_conversion_metric': (0.9892840329171609, 0.633298718670797), 'mean_module_score_metric': (0.9577698219972708, 0.606524006722232), 'module_done_rate_metric': (0.97735924634671, 0.47473193473193465), 'module_drop_on_rate_metric': (0.00186112814115757, 0.34964438122332847), 'time_spent_metric': (0.0, 1.0), 'number_of_students_infometric': (1561.1, 7478.699999999999), 'cert_rate_among_nontransfered_metric': (0.4038245904025281, 0.05420833333333327)}, 4: {'avg_try_count': (1.25, 9.689423076923076), 'done_rate_by_media': (0.767865539632781, 0.2964470238516526), 'done_rate_by_prev_element_metric': (1.0, 0.6757257971238), 'done_rate_by_pupils': (1.0, 0.7962962962962963), 'done_in_first_try_rate_metric': (0.9436078006500541, 0.4620065789473684), 'avg_solve_improvement_time_metric': (0.6801716583333335, 39.760632186666655), 'number_of_module_students_infometric': (64.05, 3002.5999999999995), 'achieved_in_module_number_infometric': (42.0, 1484.3999999999999), 'module_conversion_metric': (0.9892840329171609, 0.633298718670797), 'mean_module_score_metric': (0.9577698219972708, 0.606524006722232), 'module_done_rate_metric': (0.97735924634671, 0.47473193473193465), 'module_drop_on_rate_metric': (0.00186112814115757, 0.34964438122332847), 'time_spent_metric': (0.0, 1.0), 'number_of_students_infometric': (1561.1, 7478.699999999999), 'cert_rate_among_nontransfered_metric': (0.4038245904025281, 0.05420833333333327)}, 5: {'avg_try_count': (1.25, 9.689423076923076), 'done_rate_by_media': (0.767865539632781, 0.2964470238516526), 'done_rate_by_prev_element_metric': (1.0, 0.6757257971238), 'done_rate_by_pupils': (1.0, 0.7962962962962963), 'done_in_first_try_rate_metric': (0.9436078006500541, 0.4620065789473684), 'avg_solve_improvement_time_metric': (0.6801716583333335, 39.760632186666655), 'number_of_module_students_infometric': (64.05, 3002.5999999999995), 'achieved_in_module_number_infometric': (42.0, 1484.3999999999999), 'module_conversion_metric': (0.9892840329171609, 0.633298718670797), 'mean_module_score_metric': (0.9577698219972708, 0.606524006722232), 'module_done_rate_metric': (0.97735924634671, 0.47473193473193465), 'module_drop_on_rate_metric': (0.00186112814115757, 0.34964438122332847), 'time_spent_metric': (0.0, 1.0), 'number_of_students_infometric': (1561.1, 7478.699999999999), 'cert_rate_among_nontransfered_metric': (0.4038245904025281, 0.05420833333333327)}}
metrics_minmax = {
    1: {                         # Green    Red
        'module_conversion_metric': (0.9, 0.8),
        'mean_module_score_metric': (0.8, 0.65),
        'module_drop_on_rate_metric': (0.03, 0.065),
        'time_spent_metric' : (0.5, 0.99),
        'avg_try_count': (9, 12),
        'done_rate_by_media': (0.2, 0.16),
        'done_rate_by_prev_element_metric': (0.65, 0.56),
        'done_in_first_try_rate_metric': (0.55, 0.45),
        'avg_solve_improvement_time_metric': (35, 50),
        'time_between_tries_clip_metric': (7, 9)
    },
    2: {                         # Green    Red
        'module_conversion_metric': (0.85, 0.61),
        'mean_module_score_metric': (0.75, 0.6),
        'module_drop_on_rate_metric': (0.06, 0.1),
        'time_spent_metric' : (0.65, 0.99),
        'avg_try_count': (3.25, 4),
        'done_rate_by_media': (0.25, 0.2),
        'done_rate_by_prev_element_metric': (0.56, 0.5),
        'done_in_first_try_rate_metric': (0.4, 0.3),
        'avg_solve_improvement_time_metric': (47, 53),
        'time_between_tries_clip_metric': (16, 17)
    },
    3: {                         # Green    Red
        'module_conversion_metric': (0.9, 0.82),
        'mean_module_score_metric': (0.75, 0.7),
        'module_drop_on_rate_metric': (0.02, 0.04),
        'time_spent_metric' : (0.48, 0.99),
        'avg_try_count': (14, 17),
        'done_rate_by_media': (0.28, 0.2),
        'done_rate_by_prev_element_metric': (0.56, 0.5),
        'done_in_first_try_rate_metric': (0.34, 0.26),
        'avg_solve_improvement_time_metric': (70, 76),
        'time_between_tries_clip_metric': (10, 12)
    },
    4: {                         # Green    Red
        'module_conversion_metric': (0.86, 0.8),
        'mean_module_score_metric': (0.77, 0.72),
        'module_drop_on_rate_metric': (0.03, 0.055),
        'time_spent_metric' : (0.3, 0.99),
        'avg_try_count': (15, 17),
        'done_rate_by_media': (0.35, 0.3),
        'done_rate_by_prev_element_metric': (0.6, 0.5),
        'done_in_first_try_rate_metric': (0.34, 0.3),
        'avg_solve_improvement_time_metric': (50, 55),
        'time_between_tries_clip_metric': (7, 9)
    },
    5: {                         # Green    Red
        'module_conversion_metric': (0.95, 0.9),
        'mean_module_score_metric': (0.88, 0.86),
        'module_drop_on_rate_metric': (0.04, 0.05),
        'time_spent_metric' : (0.5, 0.99),
        'avg_try_count': (15, 18),
        'done_rate_by_media': (0.4, 0.35),
        'done_rate_by_prev_element_metric': (0.65, 0.6),
        'done_in_first_try_rate_metric': (0.47, 0.41),
        'avg_solve_improvement_time_metric': (50, 55),
        'time_between_tries_clip_metric': (4.5, 6)
    },
    6: {                         # Green    Red
        'module_conversion_metric': (0.95, 0.94),
        'mean_module_score_metric': (0.87, 0.83),
        'module_drop_on_rate_metric': (0.02, 0.05),
        'time_spent_metric' : (0.5, 0.99),
        'avg_try_count': (7, 10),
        'done_rate_by_media': (0.47, 0.45),
        'done_rate_by_prev_element_metric': (0.82, 0.7),
        'done_in_first_try_rate_metric': (0.4, 0.3),
        'avg_solve_improvement_time_metric': (19, 25),
        'time_between_tries_clip_metric': (3.9, 4.5)
    }
}


chart_size = (14, 4)
chart_disabled = "lightgray"

emojis = {
    "text": "📃",
    "video": "🎥",
    "link": "🔗"
}

fillcolors = (0, 255, 0), (255, 255, 0), (255, 0, 0)
default_color = "#ffffff"
