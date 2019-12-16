// #include <Eigen/LU>


int add(int i, int j);


/**
 * @brief      Multiply all entries by 2
 *
 * @param[in]  input  std::vector read only
 *
 * @return     std::vector new copy
 */
std::vector<double> modify(const std::vector<double>& input);


std::vector<int> multiply(const std::vector<double>& input);

std::vector<double> length(const std::vector<double>& pos);

Eigen::MatrixXd inv(const Eigen::MatrixXd &xs);

double det(const Eigen::MatrixXd &xs);

class CustomVectorXd
{
private:

  Eigen::VectorXd m_data;

public:

  CustomVectorXd(const Eigen::VectorXd &data);

  Eigen::VectorXd mul(double factor=1.);

};
