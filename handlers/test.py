data_list = [11,8,6,3,-3,-6]

def listpuls(data_list):
        data_list.reverse()
        length = len(data_list)
        results = []
        for i in range(1,length):
            results.append(data_list[i]-data_list[i-1])
        print results
        return results


listpuls(data_list)