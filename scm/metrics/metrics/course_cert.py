
import pandas as pd

# ~ class CertRateAmongAllStudentsMetric:
    # ~ description = """Процент получивших сертификаты"""
    
    # ~ def cnt_of_certificate(data, config):
        # ~ ans = pd.DataFrame(columns=['course_id', 'count_of_certificate', 'value', 'sample'])
        # ~ modules = len(data.course_module['id'][(data.course_module.is_advanced == False) & (data.course_module.level == 1)])
        # ~ crf = 0
        # ~ achieve = pd.merge(data.course_module[['id', 'course_id', 'is_advanced', 'level']], data.user_module_progress[['user_id', 'course_id', 'course_module_id', 'is_achieved']], left_on=['id', 'course_id'], right_on=['course_module_id', 'course_id'], how='left').query('is_advanced == False and is_achieved == True and level == 1').drop(columns=['id', 'is_advanced', 'is_achieved', 'level'])
        # ~ for user_id, group in achieve.groupby('user_id'):
            # ~ if len(group) == modules:
                # ~ crf += 1
        # ~ d = {'course_id': data.course.id.iloc[0], 'count_of_certificate': crf, 'value': crf / len(set(data.user_module_progress['user_id'])), 'sample': len(set(data.user_module_progress['user_id']))}
        # ~ ans = ans.append(d, ignore_index=True)
        # ~ ans = ans.astype({'id': int, 'count_of_certificate': int, 'sample': int})
        # ~ return ans


# ~ class CertRateAmongStudentsWhoStayed:
    # ~ description = """Процент получивших сертификаты среди тех, кто прошел хотя бы один модуль"""
    
    # ~ def calc(data, config):
        # ~ ans = pd.DataFrame(columns=['id', 'count_of_certificate', 'value', 'sample'])
        # ~ modules = set(data.course_module['id'][(data.course_module.is_advanced == False) & (data.course_module.level == 1)])
        # ~ first_module = list(modules - set(data.course_graph.to_module_id))
        # ~ crf = 0
        # ~ achieve = pd.merge(data.course_module[['id', 'course_id', 'is_advanced', 'level']], data.user_module_progress[['user_id', 'course_id', 'course_module_id', 'is_achieved']], left_on=['id', 'course_id'], right_on=['course_module_id', 'course_id'], how='left').query('is_advanced == False and level == 1').drop(columns=['id', 'is_advanced', 'level'])
        # ~ cnt = len(set(achieve.user_id))
        # ~ for user_id, group in achieve.groupby('user_id'):
            # ~ if all(group['is_achieved']) and len(group) == len(modules):
                # ~ crf += 1
            # ~ else:
                # ~ f = False
                # ~ for f_mod in first_module:
                    # ~ if not group[(group.course_module_id == f_mod)]['is_achieved'].item():
                        # ~ f = True
                        # ~ break
                # ~ cnt -= f
        # ~ d = {'id': data.course.id.iloc[0], 'count_of_certificate': crf, 'value': crf / cnt, 'sample': cnt}
        # ~ ans = ans.append(d, ignore_index=True)
        # ~ ans = ans.astype({'id': int, 'count_of_certificate': int, 'sample': int})
        # ~ return ans

from scm.metrics.decorators import metric

@metric.course(name="Процент получивших сертификаты", id="cert_rate_among_nontransfered_metric")
class CertRateExceptingTransfered:
    description = """Процент получивших сертификаты среди тех, кто прошел хотя бы один модуль, игнорируя сертификаты за перенос прогресса"""
    
    # Author: Arina
    @staticmethod
    def calc(data, config):
        ans = pd.DataFrame(columns=['id', 'count_of_certificate', 'value', 'count_of_transferred', 'sample'])
        modules = set(data.course_module['id'][(data.course_module.type == 'ordinary') & (data.course_module.level == 1)])
        first_module = list(modules - set(data.course_graph.to_module_id))
        crf = 0
        achieve = pd.merge(data.course_module[['id', 'course_id', 'is_advanced', 'level']], data.user_module_progress[['user_id', 'course_id', 'course_module_id', 'is_achieved']], left_on=['id', 'course_id'], right_on=['course_module_id', 'course_id'], how='left').query('is_advanced == False and level == 1').drop(columns=['id', 'is_advanced', 'level'])
        cnt = len(set(achieve.user_id))
        cnt_tr = 0
        not_advanced_elements = pd.merge(data.user_element_progress[['course_id', 'course_module_id', 'course_element_id']], data.course_element[['module_id', 'element_id', 'is_advanced', 'element_type']], left_on=['course_module_id', 'course_element_id'], right_on=['module_id', 'element_id'], how='left').query('(is_advanced == False) and (element_type == "task")').drop(columns=['element_type', 'is_advanced', 'module_id', 'element_id']).rename(columns={'course_module_id': 'module_id', 'course_element_id': 'element_id'}).groupby(['course_id', 'module_id']).agg(set)
        for user_id, group in achieve.groupby('user_id'):
            if all(group['is_achieved']) and len(group) == len(modules):
                mod_tr = 0
                for module, group2 in data.user_element_progress[(data.user_element_progress.achieve_reason == 'transferred') & (data.user_element_progress.user_id == user_id)].groupby('course_module_id'):
                    if module in modules:
                        cnt_el = not_advanced_elements.query(f'module_id == {module}')['element_id'].item() & set(group2['course_element_id'])
                        user_score = 0
                        for el in cnt_el:
                            user_score += data.course_element[(data.course_element.module_id == module) & (data.course_element.element_id == el)]['score'].item()
                        if user_score / data.course_module[data.course_module.id == module]['progress_max'].item() * 100 >= data.course_module[data.course_module.id == module]['percent_to_pass'].item():
                            mod_tr += 1
                        else:
                            break
                if mod_tr == len(modules):
                    cnt -= 1
                    cnt_tr += 1
                else:
                    crf += 1
            else:
                f = False
                for f_mod in first_module:
                    if not group[(group.course_module_id == f_mod)]['is_achieved'].item():
                        f = True
                if f:
                    cnt -= 1
        d = {'id': data.course.id.iloc[0], 'count_of_certificate': crf, 'value': crf / cnt, 'count_of_transferred': cnt_tr, 'sample': cnt}
        ans = ans.append(d, ignore_index=True)
        ans = ans.astype({'id': int, 'count_of_certificate': int, 'count_of_transferred': int, 'sample': int})
        return ans
