import unittest

from data_point import DataPoint
from kmeans import KMeans

class KMeansTestCase(unittest.TestCase):
    def test_random_centroids(self):
        '''测试不传入初始中心点时
        会创建随机中心点'''
        point1: DataPoint = DataPoint([2.0,1.0,1.0])
        point2: DataPoint = DataPoint([2.0,2.0,5.0])
        point3: DataPoint = DataPoint([3.0,1.5,2.5])
        kmeans: KMeans = KMeans(2,[point1,point2,point3])
        self.assertIsNotNone(kmeans._centroids)


    def test_given_right_centroids(self):
        '''测试传入了数量正确的初始中心点时
        初始中心点会被正确设置'''
        point1: DataPoint = DataPoint([2.0,1.0,1.0])
        point2: DataPoint = DataPoint([2.0,2.0,5.0])
        point3: DataPoint = DataPoint([3.0,1.5,2.5])
        centroid1: DataPoint = DataPoint([1.0,1.0,1.0])
        centroid2: DataPoint = DataPoint([2.0,2.0,2.0])
        kmeans: KMeans = KMeans(2,[point1,point2,point3],
                               [centroid1,centroid2])
        self.assertEqual(kmeans._centroids,[centroid1,centroid2])
    
    def test_wrong_centroids_number(self):
        '''测试传入的初始中心点数量和k不一致时
        会抛出ValueError异常'''
        point1: DataPoint = DataPoint([2.0,1.0,1.0])
        point2: DataPoint = DataPoint([2.0,2.0,5.0])
        point3: DataPoint = DataPoint([3.0,1.5,2.5])
        centroid: DataPoint = DataPoint([1.0,1.0,1.0])
        self.assertRaises(ValueError,
                          KMeans,
                          2,[point1,point2,point3],[centroid])
    


if __name__ == '__main__':
    unittest.main()
