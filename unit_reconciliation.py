import pandas as pd
import re
from decimal import Decimal as D
import numpy as np

class UnitReconciliation:
    
    def __init__(self, data):
        '''
            initialize class with the data. 
            manipulate and assign the data for further intercations 
        '''

        # regex pattern breakdown:
        # D \d+ - == find a word that starts with the letter 'D' leading with any amount of digits following the symbol '-'
        # (?: POS | TRN ) == following with the word 'POS' or 'TRN'. (?: ... ) refers to a non capturing group
        # .* ? == (.*) continue capturing any character, (?) until the first occurrence of next statement.
        # (?= D\d+- | $ ) == (?= ... ) don't capture the enclosed statement as part of the match. 
        # and stop the match at a new occurrence of this pattern (d\d+-) or at the end of the file ($)
        pattern = '(D\d+-(?:POS|TRN).*?(?=D\d+-|$))'

        # separate and apply records (e.g. D0-POS...) to a list
        # re.DOTALL incudes new lines (\n) to the '.' operator
        data_list = re.findall(pattern, data, re.DOTALL)

        # set record type (e.g. D0-POS) to a dictionary key 
        # and split record lines to a list and set it as the value
        data_dict = {row.splitlines()[0]: row.splitlines()[1:] for row in data_list}

        # convert records to a pandas DataFrame and set the record type to it's appropriate variable
        self.d0_pos = self._convert_pos_to_df(data_dict['D0-POS'])
        self.d1_trn = self._convert_trn_to_df(data_dict['D1-TRN'])
        self.d1_pos = self._convert_pos_to_df(data_dict['D1-POS'])

    @staticmethod
    def _correct_format(df):
        '''
            apply and return desired format to a pandas DataFrame
        '''

        df.index.name = None # remove index name
        return df.replace(0, np.nan).dropna() # drop rows with 0 or nan value

    def _convert_pos_to_df(self, position_list): 
        '''
            convert list with space seperated records to a pandas DataFrame. (used for position record type).
            input: position_list: the records in the list are expected to have two values, 1) share name, 2) Share value.
            ps. all numbers are converted to decimals (with 'D()') for accuracy.
        '''

        df = pd.DataFrame([(row.split()[0], D(row.split()[1])) for row in position_list if row.strip()])  # 'if row.strip()' checks for empty rows (e.g. '\n')
        position_df = df.groupby(0)[1].sum() # if a share is posted twice, it will sum the share value.
        return self._correct_format(position_df)

    def _convert_trn_to_df(self, transaction_list):
        '''
            convert list with space seperated records to a pandas DataFrame. (used for transaction record type).
            input: position_list: the records in the list are expected to have four values, 
            1) share name, 2) transaction type (e.g. BUY SELL), 3) Share value, 4) cash value.
            returns: a DataFrame with two columns, 1) share name, 2) Share value.
            ps. all numbers are converted to decimals (with 'D()') for accuracy.
        '''

        # remove the transaction type and modify the values to negative or positive 
        converted_list = [] 
        for transaction in transaction_list:
            tr = transaction.split()
            # check for empty rows (e.g. '\n')
            if not tr: 
                continue
            if tr[1] in ['DEPOSIT', 'DIVIDEND', 'SELL']:
                converted_list.append([tr[0], D('-'+tr[2]), D(tr[3])])
            else: # includes FEE and BUY
                converted_list.append([tr[0], D(tr[2]), D('-'+tr[3])])
        
        # convert transaction to DataFrame for easy comparison 
        df = pd.DataFrame(converted_list)
        transaction_df = df.groupby(0)[1].sum()
        total_cash = df[2].sum()
        transaction_df['Cash'] = total_cash
        return self._correct_format(transaction_df)

    def apply_transaction(self):
        '''
            apply and return the transaction to the position record of previous day.
        '''

        return self._correct_format(self.d0_pos.add(self.d1_trn, fill_value=0))

    def posted_position_reconciliation(self):
        '''
            compare applied transaction to current position and return the difference.
        '''

        calc_pos = self.apply_transaction()
        return self._correct_format(self.d1_pos.subtract(calc_pos, fill_value=0))

    def save(self, path):
        '''
            save the reconciliation to specified path 
        '''

        return self.posted_position_reconciliation().to_csv(path, sep=' ', header=False)


# do not run if imported
if __name__ == '__main__':

    with open('recon.in', 'r', encoding='utf-8') as data:
        unit_reconciliation = UnitReconciliation(data.read())
        unit_reconciliation.save('recon.out')

