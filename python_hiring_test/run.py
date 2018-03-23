"""Main script for generating output.csv."""
import pandas as pd

def main():
    df = pd.read_csv("./data/raw/pitchdata.csv", sep=',')
    
    # For Pitcher team Id
    data_pitch = df.groupby(['PitcherTeamId','HitterSide'],as_index = False)['PA','AB','H','TB','BB','SF','HBP'].sum()
    data_pitch.columns = ['SubjectId' if x=='PitcherTeamId' else x for x in data_pitch.columns]
    data_pitch['Split'] = data_pitch.HitterSide.apply(lambda x: "vs LHH" if x == 'L' else 'vs RHH')
    data_pitch['Subject'] = 'PitcherTeamId'

    # For Pitcher Id
    data_pitch_id = df.groupby(['PitcherId','HitterSide'],as_index = False)['PA','AB','H','TB','BB','SF','HBP'].sum()
    data_pitch_id.columns = ['SubjectId' if x=='PitcherId' else x for x in data_pitch_id.columns]
    data_pitch_id['Split'] = data_pitch_id.HitterSide.apply(lambda x: "vs LHH" if x == 'L' else 'vs RHH')
    data_pitch_id['Subject'] = 'PitcherId'
    
    # For Hitter team Id
    data_hitter = df.groupby(['HitterTeamId','PitcherSide'],as_index = False)['PA','AB','H','TB','BB','SF','HBP'].sum()
    data_hitter.columns = ['SubjectId' if x=='HitterTeamId' else x for x in data_hitter.columns]
    data_hitter['Split'] = data_hitter.PitcherSide.apply(lambda x: "vs LHP" if x == 'L' else 'vs RHP')
    data_hitter['Subject'] = 'HitterTeamId'
    
    # For Hitter team
    data_hitter_id = df.groupby(['HitterId','PitcherSide'],as_index = False)['PA','AB','H','TB','BB','SF','HBP'].sum()
    data_hitter_id.columns = ['SubjectId' if x=='HitterId' else x for x in data_hitter_id.columns]
    data_hitter_id['Split'] = data_hitter_id.PitcherSide.apply(lambda x: "vs LHP" if x == 'L' else 'vs RHP')
    data_hitter_id['Subject'] = 'HitterId'
    
    # Combining Hitter and Picther team
    features = ['SubjectId','Split','Subject','PA','AB','H','TB','BB','SF','HBP']
    data_combined = pd.concat([data_pitch[features],data_hitter[features],data_pitch_id[features],data_hitter_id[features]],axis = 0)
    
    data_final = data_combined[data_combined['PA']>=25]
    
    # Calculating Stats
    data_final['AVG'] = (data_final.H/ data_final.AB).round(3)
    data_final['OBP'] = ((data_final.H + data_final.BB + data_final.HBP) / (data_final.AB + data_final.BB + data_final.HBP + data_final.SF)).round(3)
    data_final['SLG'] = (data_final.TB / data_final.AB).round(3)
    data_final['OPS'] = data_final.SLG + data_final.OBP
    
    # Getting the desired shape
    data_final = pd.melt(data_final, id_vars = ['SubjectId','Split','Subject'], value_vars = ['AVG','OBP','SLG','OPS'], var_name = 'Stat',value_name = 'Value')
    
    # Exporting
    data_final.sort_values(by = ['SubjectId','Stat','Split','Subject'])[['SubjectId','Stat','Split','Subject','Value']].to_csv('./data/processed/output.csv',index = False)
    

if __name__ == '__main__':
    main()
