
language_code = "en"
df_tmp = df.loc[df.lang == language_code, :].reset_index(drop=True)
pd.options.display.max_rows = 100  # see up to 100 entries
pd.options.display.max_colwidth = 250  # widen how much text is presented of each tweet
samples = df_tmp.sample(100)
samples