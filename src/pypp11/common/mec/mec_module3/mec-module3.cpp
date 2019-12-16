//#include "tools/mec/mec_module1/mec-module1.hpp"
#include <vector>
#include <cmath>

#include <Eigen/LU>

#include "mec-module3.hpp"


int add(int i, int j) {
    return i + j;
}


std::vector<double> modify(const std::vector<double>& input)
{
  // std::vector<double> output;

  // std::transform(
  //   input.begin(),
  //   input.end(),
  //   std::back_inserter(output),
  //   [](double x) -> double { return 2.*x; }
  // );

  // // N.B. this is equivalent to (but there are also other ways to do the same)
  // //
  std::vector<double> output(input.size());

  for ( std::size_t i = 0 ; i < input.size() ; ++i )
    output[i] = 2. * input[i];

  return output;
}


std::vector<int> multiply(const std::vector<double>& input)
{
  std::vector<int> output(input.size());

  for ( std::size_t i = 0 ; i < input.size() ; ++i )
    output[i] = 10*static_cast<int>(input[i]);

  return output;
}


std::vector<double> length(const std::vector<double>& pos)
{
  std::size_t N = pos.size() / 2;

  std::vector<double> output(N*3);

  for ( std::size_t i = 0 ; i < N ; ++i ) {
    output[i*3+0] = pos[i*2+0];
    output[i*3+1] = pos[i*2+1];
    output[i*3+2] = std::pow(pos[i*2+0]*pos[i*2+1],.5);
  }

  return output;
}


Eigen::MatrixXd inv(const Eigen::MatrixXd &xs)
{
  return xs.inverse();
}

double det(const Eigen::MatrixXd &xs)
{
  return xs.determinant();
}


// class-constructor: store the input "Eigen::VectorXd"
CustomVectorXd::CustomVectorXd(const Eigen::VectorXd &data) : m_data(data)
{
}

// return the custom vector, multiplied by a factor
Eigen::VectorXd CustomVectorXd::mul(double factor)
{
  return factor*m_data;
}
