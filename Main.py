import time
import DIR
from DIR import Data

if __name__ == '__main__' :


    run_time = open("Run_time_parallel.csv","w")

    # names = ['m0', 'm1', 'm2', 'm3', 'm4', 'm5', 'm7', 'm8', 'm9', 'm10'
    #         ,'m11', 'm12', 'm13', 'm14', 'm15', 'm16', 'm17', 'm18', 'm19', 'm20'
    #         ,'m21', 'm22', 'm23', 'm24', 'm25', 'm26', 'm27', 'm28', 'm29', 'm30'
    #         ,'m31', 'm32', 'm33', 'm34', 'm35', 'm36', 'm37', 'm38', 'm39', 'm40'
    #         ,'m41', 'm42', 'm43', 'm44', 'm45', 'm46', 'm47', 'm48', 'm49', 'm50'
    #         ,'m51', 'm52', 'm56', 'm57', 'm58', 'm59', 'm60', 'm61', 'm62', 'm63'
    #         ,'m64', 'm65', 'm66', 'm68', 'm70', 'm71', 'm72', 'm73', 'm74', 'm75'
    #         ,'m76', 'm77', 'm78', 'm80', 'm81', 'm82', 'm83', 'm84', 'm85', 'm86'
    #         ,'m87', 'm88', 'm90', 'm91', 'm92', 'm93', 'm94', 'm95', 'm97', 'm98'
    #         ,'m99', 'm100', 'm101', 'm102', 'm104', 'm105', 'm106', 'm107', 'm108', 'm109'
    #         ,'m110', 'm111', 'm112', 'm113', 'm114', 'm115', 'm117', 'm120', 'm121', 'm122'
    #         ,'m123', 'm124', 'm125', 'm126', 'm127', 'm128', 'm130', 'm131', 'm132', 'm133'
    #         ,'m134', 'm137', 'm141', 'm146', 'm147', 'm148', 'm267', 'm268', 'm270', 'm271'
    #         ,'m272', 'm273', 'm276', 'm277', 'm278', 'm279', 'm280', 'm282', 'm286', 'm288'
    #         ,'m289', 'm325', 'm326', 'm327', 'm328', 'm329', 'm330', 'm331', 'm332', 'm333'
    #         ,'m334', 'm336', 'm337', 'm338', 'm339', 'm382', 'm383', 'm387', 'm389', 'm391'
    #         ,'m393', 'm394', 'm395', 'm396', 'm397', 'm398']

    names = ['m0']

    # 2 core

    for name in names :

        input_file = "data/0/"+name+"/"+name+".off"

        print "Object ID", name ,"is preparing to start."

        start = time.time()
        DIR.data = Data()
        DIR.data.prepare_data(input_file)
        DIR.data.partition_object(12)
        end = time.time()

        run_time.write("%s,%s" % (name,end-start))
        print "Preprocess time :",end-start

        start = time.time()
        DIR.run(name)
        end = time.time()

        run_time.write(",%s\n" % (end-start))
        print "Run Time :",end-start

        del DIR.data
        DIR.data = None

    run_time.close()